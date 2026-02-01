from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Body

from services.subs import BillService, get_bill_service


router = APIRouter()


@router.post('/subscribe')
async def subscribe(
    user_id: Annotated[UUID, Body()],
    plan_id: Annotated[UUID, Body()],
    bill_service: Annotated[BillService, Depends(get_bill_service)]
) -> str:
    return await bill_service.payment(
        user_id=user_id,
        plan_id=plan_id,
        return_url='https://example.com'  # TODO
    )