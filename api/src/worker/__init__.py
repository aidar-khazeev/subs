import json
import aiokafka
import logging
from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

import db.postgres
import tables
from settings import kafka_settings


logger = logging.getLogger('subs-worker')


async def run():
    kafka_consumer = aiokafka.AIOKafkaConsumer(
        'payment', 'refund',
        bootstrap_servers=kafka_settings.bootstrap_servers,
        enable_auto_commit=False
    )

    await kafka_consumer.start()

    try:
        async for msg in kafka_consumer:
            if msg.topic == 'payment':
                assert isinstance(msg.value, bytes)
                data = json.loads(msg.value)

                if data['status'] == 'succeeded':
                    extra_data = data['extra_data']
                    user_id = extra_data['user_id']
                    subscription_id = extra_data['subscription_id']

                    logger.info(f'user {user_id} payed for subscription {subscription_id}')
                    async with db.postgres.session_maker() as session, session.begin():
                        plan = (await session.execute(
                            select(tables.Plan)
                            .where(tables.Plan.id == UUID(extra_data['plan_id']))
                        )).scalar_one()
                        now = datetime.now()

                        await session.execute(
                            insert(tables.Subscription)
                            .values({
                                tables.Subscription.id: subscription_id,
                                tables.Subscription.user_id: user_id,
                                tables.Subscription.plan_id: plan.id,
                                tables.Subscription.starts_at: now,
                                tables.Subscription.ends_at: now + plan.duration,
                                tables.Subscription.payment_id: UUID(data['id'])
                            })
                            .on_conflict_do_nothing()
                        )

                elif data['status'] == 'cancelled':
                    ...  # Отправить уведомление
                else:
                    raise RuntimeError(f'Unexpected payment status: "{data["status"]}"')

            elif msg.topic == 'refund':
                ...
            else:
                raise RuntimeError(f'Unexpected topic: "{msg.topic}"')

            await kafka_consumer.commit()

    finally:
        await kafka_consumer.stop()

