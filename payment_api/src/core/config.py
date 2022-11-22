import os

from pydantic import BaseSettings, SecretStr


class DotEnvMixin(BaseSettings):
    class Config:
        env_file = '.env'


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


class PaymentSettings(DotEnvMixin):
    method_types: list = ["card"]

    class Config:
        env_prefix = 'payment_'


class StripeSecrets(DotEnvMixin):
    secret_key: SecretStr
    endpoint_secret: SecretStr
    public_key: SecretStr

    class Config:
        env_prefix = 'stripe_'


class SentrySettings(DotEnvMixin):

    dsn: str
    traces_sample_rate: float = 1.0

    class Config:
        env_prefix = 'sentry_'


class Settings(DotEnvMixin):
    uvicorn_reload: bool = True
    project_name: str = 'Payment service'
    postgres: PostgresSettings = PostgresSettings()
    sentry: SentrySettings = SentrySettings()
    jwt_secret: str = 'secret'
    jwt_algorithm: str = 'HS256'

    debug: bool = False
    secret_key: str = 'S#perS3crEt_9999'
    server_address: str = 'http://localhost:8000/'
    stripe: StripeSecrets = StripeSecrets()
    payment: PaymentSettings = PaymentSettings()
    superuser_role_name: str = 'superadmin'

    class Config:
        env_file_encoding = 'utf-8'
        use_enum_values = True


settings = Settings()
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
