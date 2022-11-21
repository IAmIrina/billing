from db.postgres import engine
from sqlalchemy import MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()


class Payment(Base):
    __table__ = Table('payments', metadata, autoload=True, autoload_with=engine)


class Subscription(Base):
    __table__ = Table('subscriptions', metadata, autoload=True, autoload_with=engine)
