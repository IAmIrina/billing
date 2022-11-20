import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from api.v1 import schemas
from services.auth import JWTBearer
from services.subscruption import SubscriptionService, get_subscription_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=schemas.SubscriptionIn, summary="Create a subscription")
async def create_subscription(
        subscription: schemas.SubscriptionIn,
        user: schemas.User = Depends(JWTBearer()),
        subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    """
    Create a subscription:

    - **title**: title to subscription
    - **description**: description to subscription
    - **price**: price to subscription
    """
    # TODO добавить проверку роли администратора
    try:
        db_subscription = await subscription_service.create_subscription(subscription=subscription)
        return schemas.SubscriptionIn(**db_subscription.__dict__)
    except IntegrityError as e:
        logger.error(e)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Subscription already registered")


@router.put("/{title}", response_model=schemas.SubscriptionIn, summary="Change a subscription")
async def change_subscription(
        title: schemas.Subscription,
        subscription: schemas.SubscriptionIn,
        user: schemas.User = Depends(JWTBearer()),
        subscription_service: SubscriptionService = Depends(get_subscription_service),
):
    """
    Change a subscription:

    - **title**: title to subscription
    - **description**: description to subscription
    - **price**: price to subscription
    """
    # TODO добавить проверку роли администратора
    db_subscription = await subscription_service.get_subscription_by_title(title.name)
    if not db_subscription:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Subscription not found")
    res = await subscription_service.change_subscription(subscription=subscription, title=title.name)
    return schemas.SubscriptionIn(**res.__dict__)
