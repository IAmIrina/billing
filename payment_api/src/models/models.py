import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class Payment(Base):
    __tablename__ = 'payments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    user_id = sqlalchemy.Column(UUID(as_uuid=True), nullable=False, index=True)
    start_date = sqlalchemy.Column(sqlalchemy.DATE, index=True)
    end_date = sqlalchemy.Column(sqlalchemy.DATE, index=True)
    subscription = sqlalchemy.Column(sqlalchemy.String, index=True)
    payment_url = sqlalchemy.Column(sqlalchemy.String)
    is_paid = sqlalchemy.Column(sqlalchemy.Boolean, index=True, default=False)


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    description = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer)


class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(UUID(as_uuid=True), primary_key=True, index=True)
    payment_system_id = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    is_recurrent_payments = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
