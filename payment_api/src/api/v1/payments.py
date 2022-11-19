import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import schemas
from api.v1.paginator import Paginator
from core.config import settings
from db.postgres import get_db
from ecom.abstract import EcomClient
# TODO сделать получение клиента из абстрактного класса
from ecom.stripe_api import get_client
from schema.product import Product, ProductData
from services import crud
from services.auth import JWTBearer

logger = logging.getLogger(__name__)
router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/", response_model=schemas.ClientSecret, summary="Create a payment")
async def create_payment(
        request: Request,
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
    # TODO все обернуть в попытку, добавить проверку что оплаченный период еще не закончился
    db_payment = await crud.get_payment(
        session,
        user_id=str(user.id),
        subscription=payment.subscription.name,
        start_date=payment.start_date
    )
    # TODO вернуть ссылку на оплату если оплаты еще не было
    # if db_payment:
    #     raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Payment already registered")

    subscription = await crud.get_subscription_by_title(session, payment.subscription.name)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Subscription not found")

    db_user = await crud.get_user(session, user.id)
    if not db_user:
        customer_id = await payment_system_client.create_customer(
            # TODO удалить заглушки для имени и почты
            name='name', email='ya@ya.ru',
            idempotency_key=str(user.id)
        )
        db_user = await crud.create_user(session, user.id, payment_system_id=customer_id, is_recurrent_payments=True)

    product = Product(
        unit_amount=subscription.price,
        currency='usd',
        product_data=ProductData(name=subscription.title, description=subscription.description)
    )

    try:
        intent_id, client_secret = await payment_system_client.create_payment_intent(
            customer_id=db_user.payment_system_id,
            product=product,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Error while getting payment link")

    user_payment = schemas.UserPayment(
        user_id=user.id,
        intent_id=intent_id,
        client_secret=client_secret,
        **payment.dict()
    )
    # TODO записать сумму в базу
    await crud.create_payment(session, user_payment)

    if not settings.debug:
        return schemas.ClientSecret(data=client_secret)
    else:
        return templates.TemplateResponse(
            "checkout.html",
            {
                "request": request,
                'CLIENT_SECRET': client_secret,
                'SUBMIT_CAPTION': f"Pay {product.unit_amount / 100} {product.currency}"
            }
        )


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
