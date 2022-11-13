import os

from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    user: str = 'postgres'
    password: str = 'password'
    host: str = 'localhost'
    port: int = 5432
    db: str = 'payments'

    @property
    def dsn(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    uvicorn_reload: bool = True
    project_name: str = 'Payment service'
    postgres: PostgresSettings = PostgresSettings()
    jwt_secret: str = 'secret'
    jwt_algorithm: str = 'HS256'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        use_enum_values = True


settings = Settings()
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
