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
        .offset(offset*limit)
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
        payment_url=user_payment.payment_url,
    )
    session.add(db_payment)
    await session.commit()
    await session.refresh(db_payment)
    return db_payment
