from uuid import UUID
from http import HTTPStatus
import logging

import aiohttp


logger = logging.getLogger(__name__)


class PaymentNotifier:
    """Отправляет сообщение с помощью сервиса Уведомлений"""

    def __init__(
            self,
            notification_url: str,
            login_url: str,
            user_info_url: str,
            superuser_email: str,
            superuser_pass: str):
        self.notification_url = notification_url
        self.login_url = login_url
        self.user_info_url = user_info_url
        self.superuser_email = superuser_email
        self.superuser_pass = superuser_pass
        self.superuser_access_token = None

    @staticmethod
    async def _send_async_request(method: str, url: str, **kwargs):
        """Отправляет асинхронный запрос на указанный URL"""
        conn = aiohttp.TCPConnector(limit_per_host=5)
        async with aiohttp.ClientSession(connector=conn, trust_env=True) as session:
            try:
                request_method = getattr(session, method)
            except (ValueError, AttributeError):
                logger.warning('Unhandled request type %s', method)
                return
            return await request_method(url, **kwargs)

    async def _get_superuser_access_token(self) -> None:
        """Позволяет обновить access token Суперюзера"""
        payload = {"email": self.superuser_email, "password": self.superuser_pass}
        response = await self._send_async_request('post', self.login_url, json=payload)
        # Обрабатываем ответ
        if response.status == HTTPStatus.OK:
            # Получаем access token
            data = await response.json()
            access_token = data["access_token"]
            logging.warning("Admin did login")

            self.superuser_access_token = access_token

            return None

    async def _get_email(self, user_id: UUID, url: str):
        """Позволяет получить емэйл Пользователя из сервиса Авторизации"""
        if not self.superuser_access_token:
            await self._get_superuser_access_token()
        headers = {"Authorization": f"Bearer {self.superuser_access_token}"}
        response = await self._send_async_request('post', url, headers=headers)
        return response['email']

    async def send_notification(self, users: list[UUID], template_name: str) -> None:
        """Позволяет отправить сообщения для Пользователей"""
        emails = []
        for user in users:
            # Получаем емэйл Пользователя
            email = self._get_email(user, self.user_info_url + str(user))
            emails.append(email)
        # Отправляем запрос
        payload = {"emails": [emails], "template": template_name}
        await self._send_async_request('post', self.notification_url, json=payload)
