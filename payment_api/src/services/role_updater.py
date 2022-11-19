from uuid import UUID
import datetime as dt
from http import HTTPStatus
import logging

import aiohttp


class RoleUpdater:
    """Добавляет и удаляет роли Пользователя, используя сервис Авторизации"""
    def __init__(self,
            roles_url: str,
            login_url: str,
            superuser_email: str,
            superuser_pass: str,
            ):
        self.roles_url = roles_url
        self.login_url = login_url
        self.superuser_email = superuser_email
        self.superuser_pass = superuser_pass
        self.superuser_access_token = None

    async def _send_async_request(self, method: str, url: str, **kwargs):
        """Отправляет асинхронный запрос на указанный URL"""
        async with aiohttp.ClientSession() as session:
            match method:
                case "GET":
                    response = await session.get(url, **kwargs)
                    return response
                case "POST":
                    response = await session.post(url, **kwargs)
                    return response
                case "DELETE":
                    response = await session.delete(url, **kwargs)
                    return response

    async def _get_superuser_access_token(self) -> None:
        """Позволяет обновить access token Суперюзера"""
        # Отправляем запрос
        payload = {"email": self.superuser_email, "password": self.superuser_pass}
        response = await self._send_async_request(
            "POST",
            self.login_url,
            json=payload
        )
        # Обрабатываем ответ
        if response.status == HTTPStatus.OK:
            # Получаем access token
            data = await response.json()
            access_token = data["access_token"]
            logging.warning("Admin did login")
            # Сохраняем access_token
            self.superuser_access_token = access_token

            return None

    async def get_roles(self, user_id):
        # TODO Удалить
        url = f"{self.roles_url}{user_id}/roles"
        if not self.superuser_access_token:
            await self._get_superuser_access_token()
        headers = {
            "Authorization": f"Bearer {self.superuser_access_token}"
        }
        response = await self._send_async_request("GET", url, headers=headers)
        print(await response.text())
        return None

    async def add_roles(self, users: list[UUID], roles: list[str]):
        """Позволяет разом добавить Роли списку Пользователей"""
        # Для каждого Пользователя и для каждой Роли:
        for user in users:
            for role in roles:
                url = f"{self.roles_url}{user}/roles"
                # Если мы не запрашивали access token
                if not self.superuser_access_token:
                    await self._get_superuser_access_token()
                # Формируем данные для запроса
                headers = {"Authorization": f"Bearer {self.superuser_access_token}"}
                payload = {"name": role, "date": str(dt.datetime.now().date())}
                # Отправляем запрос
                response = await self._send_async_request("POST", url, json=payload, headers=headers)
                # Если Access Token потерял актуальность, то обновляем его и переотправляем запрос
                if response.status == HTTPStatus.FORBIDDEN:
                    await self._get_superuser_access_token()
                    await self._send_async_request("POST", url, json=payload, headers=headers)

    async def add_user(self, email: str, password: str):
        """Позволяет зарегистрировать Нового Пользователя"""
        url = "http://127.0.0.1:8999/auth/api/v1/users/register"
        payload = {"email": email, "password": password}
        response = await self._send_async_request("POST", url, json=payload)
        print(await response.text())

    async def remove_roles(self, users: list[UUID], roles: list[str]):
        """Позволяет убрать выбранные роли у списка Пользователей"""
        # Для каждого Пользователя и для каждой Роли:
        for user in users:
            for role in roles:
                url = f"{self.roles_url}{user}/roles"
                # Если мы не запрашивали access token, то перезапрашиваем
                if not self.superuser_access_token:
                    await self._get_superuser_access_token()
                # Формируем данные для запроса
                headers = {"Authorization": f"Bearer {self.superuser_access_token}"}
                payload = {"name": role, "date": str(dt.datetime.now().date())}
                # Отправляем запрос
                response = await self._send_async_request("DELETE", url, json=payload, headers=headers)
                # Если Access Token потерял актуальность, то обновляем его и переотправляем запрос
                print(response.status)
                print(await response.text())
                if response.status == HTTPStatus.FORBIDDEN:
                    await self._get_superuser_access_token()
                    await self._send_async_request("DELETE", url, json=payload, headers=headers)

