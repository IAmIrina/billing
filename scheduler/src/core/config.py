from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    db: str = Field(..., env='POSTGRES_DB')
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')
    information_period: int = Field(..., env='INFORMATION_PERIOD')

    class Config:
        env_file = '../../.env'


db_settings = PostgresSettings()
