import os

from pydantic import BaseSettings, SecretStr, Field
import logging

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
    secret_key: SecretStr = 'sk_test_key'
    endpoint_secret: SecretStr = 'pk_test_51M2zGaEUp1F2G8nCjwz4CIQDmbYMnwQov5GiD4fUbGq0WPN4BMXXrSPOI3GvcFdibmskQTG8UMswD2Yp4iSqWNwK00aCATDahk'
    public_key: SecretStr = 'whsec_endpoint'

    class Config:
        env_prefix = 'stripe_'


class AuthSettings(DotEnvMixin):
    auth_host: str = Field("localhost", env='AUTH_HOST')
    auth_port: int = Field(8999, env='AUTH_PORT')
    superuser_email: str = Field("alexvkleschov@gmail.com", env='AUTH_SUPERUSER_EMAIL')
    superuser_password: str = Field(..., env='AUTH_SUPERUSER_PASSWORD')
    roles_path: str = Field("/auth/api/v1/users/", env='AUTH_ROLES_PATH')
    login_path: str = Field("/auth/api/v1/auth/login", env='AUTH_LOGIN_PATH')

    @property
    def roles_url(self):
        return f"http://{self.auth_host}:{self.auth_port}{self.roles_path}"

    @property
    def login_url(self):
        return f"http://{self.auth_host}:{self.auth_port}{self.login_path}"


class Settings(DotEnvMixin):
    uvicorn_reload: bool = True
    project_name: str = 'Payment service'
    postgres: PostgresSettings = PostgresSettings()
    jwt_secret: str = 'secret'
    jwt_algorithm: str = 'HS256'

    debug: bool = False
    secret_key: str = 'S#perS3crEt_9999'
    server_address: str = 'http://localhost:8000/'
    stripe: StripeSecrets = StripeSecrets()
    payment: PaymentSettings = PaymentSettings()
    auth: AuthSettings = AuthSettings()

    class Config:
        env_file_encoding = 'utf-8'
        use_enum_values = True


settings = Settings()
logging.warning(settings)
logging.warning(settings.auth.login_url)
# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
