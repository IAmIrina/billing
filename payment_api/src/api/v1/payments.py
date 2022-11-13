from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import schemas
from db.postgres import get_db
from services.auth import JWTBearer
from services import crud

router = APIRouter()


@router.post("/", response_model=schemas.PaymentUrl, summary="Create a payment")
async def create_payment(
        payment: schemas.Payment,
        user: schemas.User = Depends(JWTBearer()),
        session: AsyncSession = Depends(get_db)
):
    """
    Create a payment for subscription and return url for payment by user:

    - **subscription**: subscription title
    - **start_date**: date of start subscription
    """
    # TODO все обернуть в попытку
    db_payment = await crud.get_payment(
        session,
        user_id=str(user.id),
        subscription=payment.subscription.name,
        start_date=payment.start_date
    )

    if db_payment:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Payment already registered")

    try:
        # TODO заменить на получение адреса из сервиса
        payment_url = 'https://pydantic-docs.helpmanual.io/usage/types/#standard-library-types'
    except:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error while getting payment link")

    user_payment = schemas.UserPayment(
        user_id=user.id,
        payment_url=payment_url,
        **payment.dict()
    )
    await crud.create_payment(session, user_payment)

    return schemas.PaymentUrl(payment_url=payment_url)
