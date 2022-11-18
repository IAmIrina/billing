from enum import Enum
from typing import Union

from schema.mixins import OrjsonModel


class RefundReason(Enum):
    duplicate = 'Duplicate'
    fraudulent = 'Fraud'
    requested_by_customer = 'Requested'


class CancelReason(Enum):
    duplicate = 'Duplicate'
    fraudulent = 'Fraud'
    abandoned = 'Abandoned'


class PaymentIntent(OrjsonModel):
    payment_intent: str
    customer: str
    status: str

    class Config:
        orm_mode = True


class RefundedCharge(OrjsonModel):
    charge_id: str
    payment_intent: str
    status: str


class Event(Enum):
    charge_refunded = 'charge.refunded'
    payment_intent_canceled = 'payment_intent.canceled'
    payment_intent_succeeded = 'payment_intent.succeeded'


class PaymentEvent(OrjsonModel):
    type: Event
    data: Union[PaymentIntent, RefundedCharge]
    row_data: dict
