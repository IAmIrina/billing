import time

from services.role_updater import RoleUpdater


class PaymentManager:
    """Управляет обработкой успешной транзакции и взаимодействует с другими сервисами"""
    def __init__(self, auth_updater: RoleUpdater, enricher, model_to_process):
        self.auth_updater = auth_updater
        self.enricher = enricher
        self._model_to_process = model_to_process

    async def watch_payments(self):
        """Мониторит новые записи в БД"""
        while True:
            time.sleep(2)
            result = await self.enricher.get_payments_by_intent(self._model_to_process, payment_intent="test_intent1")
            print("Works!")
            print(result)


    def update_roles(self):
        """Изменяет Роли"""
        pass

    def send_notifications(self):
        """Отправляет Уведомления"""
        pass
