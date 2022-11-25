import logging
import asyncio

from core.config import settings
from services.data_enricher import DataEnricher
from services.role_updater import RoleUpdater
from services.notifier import PaymentNotifier
from services.payment_manager import PaymentManager
from models.models import Event


logger = logging.getLogger(__name__)

# Инициализируем компоненты и сам объект-менеджер, который будет обрабатывать оплаты
enricher = DataEnricher()
updater = RoleUpdater(
    roles_url=settings.auth.roles_url,
    login_url=settings.auth.login_url,
    superuser_email=settings.auth.superuser_email,
    superuser_pass=settings.auth.superuser_password,
)
notifier = PaymentNotifier(
    notification_url=settings.notification.notification_url,
    login_url=settings.auth.login_url,
    user_info_url=settings.auth.user_info_url,
    superuser_email=settings.auth.superuser_email,
    superuser_pass=settings.auth.superuser_password,
)
manager = PaymentManager(
    auth_updater=updater,
    enricher=enricher,
    notifier=notifier,
    model_to_process=Event
)

if __name__ == "__main__":
    logger.warning("Payment Manager Started")
    asyncio.run(manager.watch_events())
