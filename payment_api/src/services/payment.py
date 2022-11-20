from functools import lru_cache

from dateutil.relativedelta import relativedelta
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.v1 import schemas
from db.postgres import get_db
from models import models
from services.base import BaseService


class PaymentService(BaseService):

    async def get_payment(self, user_id, start_date, subscription):
        """Функция ищет оплаченный платеж пользователя по подписке с датой окончания больше,
         чем дата старта, указанная в аргументе"""

        result = await self.session.execute(select(models.Payment).where(
            models.Payment.user_id == user_id,
            start_date < models.Payment.end_date,
            models.Payment.subscription == subscription,
            models.Payment.is_paid
        ))
        return result.scalars().first()

    async def get_paid_payments(self, user_id, offset=1, limit=1, ):
        """Функция получает все оплаченные платежи пользователя"""
        result = await self.session.execute(
            select(models.Payment)
            .where(
                models.Payment.user_id == user_id,
                # FIXME закомментировал для отладки
                # models.Payment.is_paid,
            )
            .offset(offset * limit)
            .limit(limit)
            .order_by(models.Payment.id)
        )
        return result.scalars().all()

    async def create_payment(self, user_payment: schemas.UserPayment):
        db_payment = models.Payment(
            user_id=user_payment.user_id,
            start_date=user_payment.start_date,
            end_date=user_payment.start_date + relativedelta(months=1, days=-1),
            subscription=user_payment.subscription.name,
            client_secret=user_payment.client_secret,
            intent_id=user_payment.intent_id,
        )
        self.session.add(db_payment)
        await self.session.commit()
        await self.session.refresh(db_payment)
        return db_payment


@lru_cache()
def get_payment_service(session: AsyncSession = Depends(get_db)) -> PaymentService:
    return PaymentService(session)
