import time
import logging
from uuid import UUID

from src.services.role_updater import RoleUpdater
from src.services.data_enricher import DataEnricher


logger = logging.getLogger(__name__)


class PaymentManager:
    """Управляет обработкой успешной транзакции и взаимодействует с другими сервисами"""
    def __init__(self, auth_updater: RoleUpdater, enricher: DataEnricher, model_to_process):
        self._auth_updater = auth_updater
        self._enricher = enricher
        self._model_to_process = model_to_process

    async def watch_events(self) -> None:
        """Мониторит новые необработанные записи в БД"""
        while True:
            # TODO Нормально переписать паузу между получением Ивентов
            time.sleep(5)
            # TODO Переписать логику с использованием реальной data Страйпа
            # TODO Список ролей также получать из реальной базы со связкой Подписка-Роли
            logger.warning("Watch New Events")
            payments = await self._enricher.get_uncompleted_events(self._model_to_process)
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
        await self._auth_updater.add_roles(users=users, roles=roles)

    async def mark_as_completed(self, id: UUID) -> None:
        """Помечает Оплату как завершенную"""
        await self._enricher.mark_event_as_completed(self._model_to_process, id, completed=True)
        logger.warning(f"Payment Management Completed on payment {id}")

    def send_notifications(self) -> None:
        """Отправляет Уведомления через сервис уведомлений"""
        raise NotImplementedError

