import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres import Base


class PaymentToProcess(Base):
    """
    Таблица для Успешных Оплат/Возвратов, которые необходимо обработать внутри Проекта Movies (сменить роли и т.п.)
    """
    __tablename__ = 'paymentstoprocess'

    id = sqlalchemy.Column(UUID(as_uuid=True), nullable=False, index=True, primary_key=True)
    user_id = sqlalchemy.Column(UUID(as_uuid=True), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer)
    payment_intent = sqlalchemy.Column(sqlalchemy.String)
    completed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)