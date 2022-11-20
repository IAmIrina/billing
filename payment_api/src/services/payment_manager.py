from role_updater import RoleUpdater


class PaymentManager:
    """Управляет обработкой успешной транзакции и взаимодействует с другими сервисами"""
    def __init__(self, auth_updater: RoleUpdater):
        self.auth_updater = auth_updater

    def watch_transactions(self):
        """Мониторит новые записи в БД"""
        # while True:


    def update_roles(self):
        """Изменяет Роли"""
        pass

    def send_notifications(self):
        """Отправляет Уведомления"""
        pass
