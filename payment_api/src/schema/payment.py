from enum import Enum

from schema.mixins import OrjsonModel


class RefundReason(Enum):
    duplicate = 'Duplicate'
    fraudulent = 'Fraud'
    requested_by_customer = 'Requested'


class CancelReason(Enum):
    duplicate = 'Duplicate'
    fraudulent = 'Fraud'
    abandoned = 'Abandoned'
