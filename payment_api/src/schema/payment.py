"""Ecom models."""

from enum import Enum
from typing import Union

from schema.mixins import OrjsonModel


class RefundReason(Enum):
    duplicate = 'Duplicate'
    fraudulent = 'Fraud'
    requested_by_customer = 'Requested'

    class Config:
        orm_mode = True


class Event(Enum):
    checkout_session_completed = 'checkout.session.completed'
    checkout_session_expired = 'checkout.session.expired'
    charge_refunded = 'charge.refunded'

    class Config:
        orm_mode = True


class CompletedSession(OrjsonModel):
    session_id: str
    payment_intent: str

    class Config:
        orm_mode = True


class RefundedCharge(OrjsonModel):
    charge_id: str
    payment_intent: str


class ExpiredSession(OrjsonModel):
    session_id: str


class PaymentEvent(OrjsonModel):
    type: Event
    data: Union[CompletedSession, ExpiredSession, RefundedCharge]
    row_data: dict
