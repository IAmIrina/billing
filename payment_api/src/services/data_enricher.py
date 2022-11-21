from sqlalchemy.ext.asyncio import create_async_engine
from pydantic import BaseModel
import asyncio

from sqlalchemy.future import select
from uuid import UUID


class PaymentToProcess(BaseModel):
    """Модель для записей из таблицы paymentstoprocess"""
    id: UUID
    user_id: UUID
    price: int
    payment_intent: str


# async def async_main():
#     # Создаем асинхронный Engine
#     engine = create_async_engine("postgresql+asyncpg://postgres:password@127.0.0.1:5432/payments", echo=True)
#
#     async with engine.connect() as conn:
#         result = await conn.execute(select(models.PaymentToProcess).where(models.PaymentToProcess.price == 35))
#
#         results = result.fetchall()
#         return results
#
#
#     # Очищаем подключения
#     await engine.dispose()


class DataEnricher:
    """Обогащает данные об успешных транзакциях"""
    def __init__(self):
        self._engine = create_async_engine("postgresql+asyncpg://postgres:password@127.0.0.1:5432/payments", echo=True)

    async def get_payments_by_intent(self, model, **kwargs):
        """Получаем те оплаты, в которых совпадает указанный интент"""
        async with self._engine.connect() as conn:
            result = await conn.execute(select(model).where(model.payment_intent == kwargs["payment_intent"]))
            return result.fetchall()

        await engine.dispose()

