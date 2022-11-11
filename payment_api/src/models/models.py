import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from db.postgres import Base


class Payment(Base):
    __tablename__ = 'payments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    user_id = sqlalchemy.Column(UUID(as_uuid=True), nullable=False, index=True)
    start_date = sqlalchemy.Column(sqlalchemy.DATE, index=True)
    end_date = sqlalchemy.Column(sqlalchemy.DATE, index=True)
    subscription_type = sqlalchemy.Column(sqlalchemy.String)
