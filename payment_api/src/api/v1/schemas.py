from datetime import date
from uuid import UUID

from pydantic import BaseModel
from typing import List


class User(BaseModel):
    id: UUID
    roles: List[str]


class Payment(BaseModel):
    subscription: str
    start_date: date


class PaymentOut(Payment):
    end_date: date


class Pagination(BaseModel):
    per_page: int
    page: int


class PaymentOutSchema(BaseModel):
    meta: Pagination
    data: List[PaymentOut]


class ClientSecret(BaseModel):
    data: str


class UserPayment(Payment):
    user_id: UUID
    client_secret: str
    intent_id: str


class SubscriptionIn(BaseModel):
    title: str
    description: str
    price: int
    roles: List[str]

    class Config:
        orm_mode = True


class PaymentIntent(BaseModel):
    user_id: UUID
    intent_id: str


class WebhookResponse(BaseModel):
    success: bool


class AutoPayment(BaseModel):
    is_enable: bool
