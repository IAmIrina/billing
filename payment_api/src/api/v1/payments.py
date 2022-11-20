import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates

from api.v1 import schemas
from api.v1.paginator import Paginator
from core.config import settings
from ecom.abstract import EcomClient
# TODO сделать получение клиента из абстрактного класса
from ecom.stripe_api import get_client
from schema.product import Product, ProductData
from services.auth import JWTBearer
from services.payment import PaymentService, get_payment_service
from services.subscruption import SubscriptionService, get_subscription_service
from services.user import UserService, get_user_service

logger = logging.getLogger(__name__)
router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/", response_model=schemas.ClientSecret, summary="Create a payment")
async def create_payment(
        request: Request,
        payment: schemas.Payment,
        user: schemas.User = Depends(JWTBearer()),
        payment_system_client: EcomClient = Depends(get_client),
        person_service: PaymentService = Depends(get_payment_service),
        user_service: UserService = Depends(get_user_service),
        subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    """
    Create a payment for subscription and return url for payment by user:

    - **subscription**: subscription title
    - **start_date**: date of start subscription
    """

    db_payment = await person_service.get_payment(
        user_id=str(user.id),
        subscription=payment.subscription.name,
        start_date=payment.start_date
    )
    if db_payment:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Paid period is not yet over")

    subscription = await subscription_service.get_subscription_by_title(payment.subscription.name)
    if not subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Subscription not found")

    db_user = await user_service.get_user(user.id)
    if not db_user:
        customer_id = await payment_system_client.create_customer(
            # TODO удалить заглушки для имени и почты
            name='name', email='ya@ya.ru',
            idempotency_key=str(user.id)
        )
        db_user = await user_service.create_user(
            user_id=user.id,
            payment_system_id=customer_id,
            is_recurrent_payments=True
        )

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
    await person_service.create_payment(user_payment)

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
        person_service: PaymentService = Depends(get_payment_service),
):
    """
        Return paid payments by user:
        - **page[size]**: size of page
        - **page[number]**: number of page
        """
    db_payments = await person_service.get_paid_payments(
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
