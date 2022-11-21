from core.config import db_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(db_settings.user, db_settings.password, db_settings.host,
                                                       db_settings.port, db_settings.db)
engine = create_engine(DB_URI)
session = Session(bind=engine)
