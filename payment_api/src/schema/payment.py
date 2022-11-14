from enum import Enum


class RefundReason(Enum):
    duplicate = 'Duplicate'
    fraudulent = 'Fraud'
    requested_by_customer = 'Requested'


class Event(Enum):
    charge_succeeded = 'charge.succeeded'
    checkout_session_completed = 'checkout.session.completed'
    checkout_session_expired = 'checkout.session.expired'
    charge_refunded = 'charge.refunded'
