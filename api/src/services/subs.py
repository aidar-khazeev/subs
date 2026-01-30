from dataclasses import dataclass
from uuid import UUID, uuid4
from sqlalchemy import select
import httpx

import tables
import db.postgres


@dataclass(frozen=True)
class SubscriptionsService:
    bill_client: httpx.AsyncClient

    async def bill(self, user_id: UUID, plan_id: UUID, return_url: str) -> str:
        async with db.postgres.session_maker() as session:
            plan = (await session.execute(
                select(tables.Plan)
                .where(tables.Plan.id == plan_id)
            )).scalar_one()

        response = await self.bill_client.post(
            '/api/v1/payment',
            json={
                'user_id': str(user_id),
                'amount': str(plan.amount),
                'currency': plan.currency,
                'return_url': return_url,
                'extra_data': {
                    'user_id': str(user_id),
                    'plan_id': str(plan.id),
                    'subscription_id': str(uuid4())
                }
            }
        )
        assert response.status_code == 200, response.text
        return response.json()['confirmation_url']


def get_subscriptions_service():
    return SubscriptionsService(
        bill_client=httpx.AsyncClient(
            base_url='http://127.0.0.1:8008'
        )
    )