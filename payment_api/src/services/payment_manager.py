import time
import logging
from uuid import UUID

from services.role_updater import RoleUpdater


logger = logging.getLogger(__name__)


class PaymentManager:
    """Управляет обработкой успешной транзакции и взаимодействует с другими сервисами"""
    def __init__(self, auth_updater: RoleUpdater, enricher, model_to_process):
        self._auth_updater = auth_updater
        self._enricher = enricher
        self._model_to_process = model_to_process

    async def watch_payments(self):
        """Мониторит новые необработанные записи в БД"""
        while True:
            time.sleep(2)
            payments = await self._enricher.get_uncompleted_payments(self._model_to_process)
            # Если у нас есть необработанные
            if payments:
                for payment in payments:
                    logger.warning(f"There are uncompleted payment: {payment}")
                    await self._update_roles([payment.user_id], ['standart'])



    async def _update_roles(self, users: list[UUID], roles: list[UUID]):
        """Изменяет Роли"""
        await self._auth_updater.add_roles(
            users=users,
            roles=roles
        )
        logger.warning("Roles Updated")

    def send_notifications(self):
        """Отправляет Уведомления"""
        pass
