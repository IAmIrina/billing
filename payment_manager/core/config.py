from pydantic import BaseSettings, Field

import logging

class DotEnvMixin(BaseSettings):
    class Config:
        env_file = '.env'


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
    auth: AuthSettings = AuthSettings()


# Создаем объект Настроек
settings = Settings()
logging.warning(settings)