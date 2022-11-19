from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.v1 import schemas
from models import models


async def get_payment(session: AsyncSession, **kwargs):
    result = await session.execute(select(models.Payment).where(
        models.Payment.user_id == kwargs['user_id'],
        models.Payment.start_date == kwargs['start_date'],
        models.Payment.subscription == kwargs['subscription'],
    ))
    return result.scalars().first()


async def get_paid_payments(session: AsyncSession, offset=1, limit=1, **kwargs):
    result = await session.execute(
        select(models.Payment)
        .where(
            models.Payment.user_id == kwargs['user_id'],
            models.Payment.is_paid,
        )
        .offset(offset * limit)
        .limit(limit)
        .order_by(models.Payment.id)
    )
    return result.scalars().all()


async def create_payment(session: AsyncSession, user_payment: schemas.UserPayment):
    db_payment = models.Payment(
        user_id=user_payment.user_id,
        start_date=user_payment.start_date,
        end_date=user_payment.start_date + relativedelta(months=1, days=-1),
        subscription=user_payment.subscription.name,
        # payment_url=user_payment.payment_url,
        client_secret=user_payment.client_secret,
        intent_id=user_payment.intent_id,
    )
    session.add(db_payment)
    await session.commit()
    await session.refresh(db_payment)
    return db_payment


async def create_subscription(session: AsyncSession, subscription: schemas.SubscriptionIn):
    db_subscription = models.Subscription(
        title=subscription.title.name,
        description=subscription.description,
        price=subscription.price
    )
    session.add(db_subscription)
    await session.commit()
    await session.refresh(db_subscription)
    return db_subscription


async def get_subscription_by_title(session: AsyncSession, title):
    result = await session.execute(
        select(models.Subscription).where(models.Subscription.title == title)
    )
    return result.scalars().first()


async def change_subscription(session: AsyncSession, subscription: schemas.SubscriptionIn, title: str):
    db_subscription = await get_subscription_by_title(session, title)
    db_subscription.title = title
    db_subscription.description = subscription.description
    db_subscription.price = subscription.price
    session.add(db_subscription)
    await session.commit()
    await session.refresh(db_subscription)
    return db_subscription


async def get_user(session: AsyncSession, user_id):
    result = await session.execute(
        select(models.User).where(models.User.id == user_id)
    )
    return result.scalars().first()


async def create_user(session: AsyncSession, user_id, payment_system_id, is_recurrent_payments):
    user = models.User(
        id=user_id,
        payment_system_id=payment_system_id,
        is_recurrent_payments=is_recurrent_payments
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
