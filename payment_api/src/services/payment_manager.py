import time
import logging
from uuid import UUID

from services.role_updater import RoleUpdater
from services.data_enricher import DataEnricher


logger = logging.getLogger(__name__)


class PaymentManager:
    """Управляет обработкой успешной транзакции и взаимодействует с другими сервисами"""
    def __init__(self, auth_updater: RoleUpdater, enricher: DataEnricher, model_to_process):
        self._auth_updater = auth_updater
        self._enricher = enricher
        self._model_to_process = model_to_process

    async def watch_payments(self) -> None:
        """Мониторит новые необработанные записи в БД"""
        while True:
            time.sleep(2)

            payments = await self._enricher.get_uncompleted_payments(self._model_to_process)
            # Если у нас есть необработанные оплаты
            if payments:
                for payment in payments:
                    logger.warning(f"There are uncompleted payment: {payment}")
                    # Изменяем Роли Рользователя
                    await self._update_roles([payment.user_id], ['standart', 'premium'])
                    # Отмечаем Оплату как Завершенную
                    await self.mark_as_completed(payment.id)
            # TODO Добавить логику удаления ролей при возвратах

    async def _update_roles(self, users: list[UUID], roles: list[UUID]) -> None:
        """Изменяет Роли"""
        # TODO Добавить логику, при которой можно и удалять, и добавлять роли через эту функцию.
        await self._auth_updater.remove_roles(users=users, roles=roles)
        logger.warning("Roles Updated")

    async def mark_as_completed(self, id: UUID) -> None:
        """Помечает Оплату как завершенную"""
        await self._enricher.mark_as_completed(self._model_to_process, id, completed=True)
        logger.warning("Payment Management Completed on payment {id}")

    def send_notifications(self) -> None:
        """Отправляет Уведомления через сервис уведомлений"""
        raise NotImplementedError

