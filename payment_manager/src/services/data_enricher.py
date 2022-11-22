import logging

from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update


logger = logging.getLogger(__name__)

class DataEnricher:
    """Обрабатывает и обогащает данные об успешных Оплатах"""
    def __init__(self, db_uri: str):
        self._engine = create_async_engine(db_uri, echo=True)

    async def get_uncompleted_events(self, model):
        """Получаем те Оплаты, которые отмечены необработанными"""
        async with self._engine.connect() as conn:
            result = await conn.execute(select(model).where(model.completed == False))
            return result.fetchall()

    async def mark_event_as_completed(self, model, id, **kwargs):
        """Отмечает Оплату как успешную"""
        async with self._engine.connect() as conn:
            query = (
                sqlalchemy_update(model).where(model.id == id).values(**kwargs).execution_options(synchronize_session="fetch"))
            await conn.execute(query)
            await conn.commit()
        await self._engine.dispose()
