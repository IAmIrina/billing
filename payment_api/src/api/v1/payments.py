import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import schemas
from api.v1.paginator import Paginator
from core.config import settings
from db.postgres import get_db
from ecom.abstract import EcomClient
# TODO сделать получение клиента из абстрактного класса
from ecom.stripe_api import get_client
from schema.product import Product, ProductData
from services.auth import JWTBearer
from services import crud

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=schemas.PaymentUrl, summary="Create a payment")
async def create_payment(
        payment: schemas.Payment,
        user: schemas.User = Depends(JWTBearer()),
        payment_system_client: EcomClient = Depends(get_client),
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
    # TODO вернуть ссылку на оплату если оплаты еще не было
    if db_payment:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Payment already registered")

    subscription = await crud.get_subscription_by_title(session, payment.subscription.name)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Subscription not found")
    product = Product(
        unit_amount=subscription.price,
        currency='usd',
        product_data=ProductData(name=subscription.title, description=subscription.description)
    )

    domain_url = settings.server_address
    prefix = router.prefix

    try:
        session_id, payment_intent_id, payment_url = await payment_system_client.create_checkout_session(
            product=product,
            success_redirect=domain_url + prefix + "/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_redirect=domain_url + prefix + "/cancelled",
        )
        logger.info('create payment session ', session_id, 'session_url', payment_url)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error while getting payment link")

    user_payment = schemas.UserPayment(
        user_id=user.id,
        payment_url=payment_url,
        **payment.dict()
    )
    # TODO записать в базу ид сессии и ссылку на оплату
    await crud.create_payment(session, user_payment)

    return schemas.PaymentUrl(payment_url=payment_url)


@router.get("/", response_model=schemas.PaymentOutSchema, summary="Get paid payments")
async def get_paid_payments(
        user: schemas.User = Depends(JWTBearer()),
        paginator: Paginator = Depends(),
        session: AsyncSession = Depends(get_db)
):
    """
        Return paid payments by user:
        - **page[size]**: size of page
        - **page[number]**: number of page
        """
    db_payments = await crud.get_paid_payments(
        session,
        offset=paginator.page - 1,
        limit=paginator.per_page,
        user_id=str(user.id),
    )

    return schemas.PaymentOutSchema(
        meta=schemas.Pagination(
            page=paginator.page,
            per_page=paginator.per_page,
        ),
        data=[schemas.PaymentOut(**db_payment.__dict__) for db_payment in db_payments],
    )
