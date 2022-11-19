from uuid import UUID
import datetime as dt
from http import HTTPStatus
from enum import Enum
import logging

import aiohttp
import asyncio


class HttpMethod(Enum):
    """Класс с перечислением методов HHTP запросов"""
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


class RoleUpdater:
    """Добавляет и удаляет роли Пользователя, используя удаленный сервис Авторизации"""
    def __init__(self, roles_url: str, login_url: str, superuser_email: str, superuser_pass: str):
        self.roles_url = roles_url
        self.login_url = login_url
        self.superuser_email = superuser_email
        self.superuser_pass = superuser_pass
        self.superuser_access_token = None

    @staticmethod
    async def _send_async_request(method: HttpMethod, url: str, **kwargs):
        """Отправляет асинхронный запрос на указанный URL"""
        async with aiohttp.ClientSession() as session:
            match method:
                case HttpMethod.GET:
                    response = await session.get(url, **kwargs)
                    return response
                case HttpMethod.POST:
                    response = await session.post(url, **kwargs)
                    return response
                case HttpMethod.DELETE:
                    response = await session.delete(url, **kwargs)
                    return response
                case _:
                    logging.warning("HTTP Method: {method} is undefined")

    async def _get_superuser_access_token(self) -> None:
        """Позволяет обновить access token Суперюзера"""
        payload = {"email": self.superuser_email, "password": self.superuser_pass}
        response = await self._send_async_request(HttpMethod.POST, self.login_url, json=payload)
        # Обрабатываем ответ
        if response.status == HTTPStatus.OK:
            # Получаем access token
            data = await response.json()
            access_token = data["access_token"]
            logging.warning("Admin did login")
            # Сохраняем access_token
            self.superuser_access_token = access_token

            return None

    async def add_roles(self, users: list[UUID], roles: list[str]) -> None:
        """Позволяет разом добавить Роли списку Пользователей"""
        # Для каждого Пользователя и для каждой Роли:
        for user in users:
            for role in roles:
                url = f"{self.roles_url}{user}/roles"
                # Если мы не запрашивали access token, то следует запросить
                if not self.superuser_access_token:
                    await self._get_superuser_access_token()
                # Формируем данные для запроса
                headers = {"Authorization": f"Bearer {self.superuser_access_token}"}
                payload = {"name": role, "date": str(dt.datetime.now().date())}
                # Отправляем запрос
                response = await self._send_async_request(HttpMethod.POST, url, json=payload, headers=headers)
                # Если Access Token потерял актуальность, то обновляем его и переотправляем запрос
                if response.status == HTTPStatus.FORBIDDEN:
                    await self._get_superuser_access_token()
                    await self._send_async_request(HttpMethod.POST, url, json=payload, headers=headers)

    async def remove_roles(self, users: list[UUID], roles: list[str]) -> None:
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
                response = await self._send_async_request(HttpMethod.DELETE, url, json=payload, headers=headers)
                # Если Access Token потерял актуальность, то обновляем его и переотправляем запрос
                if response.status == HTTPStatus.FORBIDDEN:
                    await self._get_superuser_access_token()
                    await self._send_async_request(HttpMethod.DELETE, url, json=payload, headers=headers)
