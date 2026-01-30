from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Request, Depends, Body

from services.subs import SubscriptionsService, get_subscriptions_service


router = APIRouter()


@router.post('/bill')
async def bill(
    user_id: Annotated[UUID, Body()],
    plan_id: Annotated[UUID, Body()],
    subs_service: Annotated[SubscriptionsService, Depends(get_subscriptions_service)],
    request: Request
) -> str:
    return await subs_service.bill(
        user_id=user_id,
        plan_id=plan_id,
        return_url=request.headers['origin']
    )