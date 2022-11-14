from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class Subscription(Enum):
    guest = 'guest'
    standart = 'standart'
    premium = 'premium'


class User(BaseModel):
    id: UUID
    roles: list[str]


class Payment(BaseModel):
    subscription: Subscription
    start_date: date


class PaymentOut(Payment):
    end_date: date


class Pagination(BaseModel):
    per_page: int
    page: int


class PaymentOutSchema(BaseModel):
    meta: Pagination
    data: list[PaymentOut]


class PaymentUrl(BaseModel):
    payment_url: HttpUrl


class UserPayment(Payment, PaymentUrl):
    user_id: UUID
