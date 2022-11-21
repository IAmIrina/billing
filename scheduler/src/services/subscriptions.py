from datetime import datetime

from core.config import db_settings
from db.postgres import session
from models.models import Payment
from sqlalchemy import and_


def get_expiring_subscriptions():
    subscriptions = session.query(
        Payment.user_id,
        Payment.end_date).filter(and_(Payment.is_paid == True,
                                      Payment.end_date - datetime.now().date() == db_settings.information_period))
    return subscriptions
