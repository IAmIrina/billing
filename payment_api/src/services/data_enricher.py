from sqlalchemy.ext.asyncio import create_async_engine
from pydantic import BaseModel

from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update
from uuid import UUID


class PaymentToProcess(BaseModel):
    """Модель для записей из таблицы paymentstoprocess"""
    id: UUID
    user_id: UUID
    price: int
    payment_intent: str


class DataEnricher:
    """Обогащает данные об успешных транзакциях"""
    def __init__(self):
        self._engine = create_async_engine("postgresql+asyncpg://postgres:password@127.0.0.1:5432/payments", echo=True)

    async def get_payments_by_intent(self, model, **kwargs):
        """Получаем те оплаты, в которых совпадает указанный интент"""
        async with self._engine.connect() as conn:
            result = await conn.execute(select(model).where(model.payment_intent == kwargs["payment_intent"]))
            return result.fetchall()
        await self._engine.dispose()

    async def get_uncompleted_payments(self, model):
        """Получаем те оплаты, в которых совпадает указанный интент"""
        async with self._engine.connect() as conn:
            result = await conn.execute(select(model).where(model.completed == False))
            return result.fetchall()
        await self._engine.dispose()

    async def mark_as_completed(self, model, id, **kwargs):
        """Отмечаем Оплату как успешную"""
        async with self._engine.connect() as conn:
            query = (
                sqlalchemy_update(model).where(model.id == id).values(**kwargs).execution_options(synchronize_session="fetch"))
            await conn.execute(query)
            await conn.commit()
        await self._engine.dispose()

# async def change_subscription(session: AsyncSession, subscription: schemas.SubscriptionIn, title: str):
#     db_subscription = await get_subscription_by_title(session, title)
#     db_subscription.title = title
#     db_subscription.description = subscription.description
#     db_subscription.price = subscription.price
#     session.add(db_subscription)
#     await session.commit()
#     await session.refresh(db_subscription)
#     return db_subscription