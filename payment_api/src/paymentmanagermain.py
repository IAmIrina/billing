import asyncio

from models.models import PaymentToProcess
from services.data_enricher import DataEnricher
from services.payment_manager import PaymentManager
from services.role_updater import RoleUpdater


# TODO Удалить этот файл, переместить логику запуска в файл-точку входа

# Компоненты
enricher = DataEnricher()
updater = RoleUpdater(
    "http://127.0.0.1:8999/auth/api/v1/users/",
    "http://127.0.0.1:8999/auth/api/v1/auth/login",
    "alexvkleschov@gmail.com",
    "sobaka123",
)
# notificator - in production

# Объявляем менеджер
manager = PaymentManager(
    auth_updater=updater,
    enricher=enricher,
    model_to_process=PaymentToProcess
)

# Постоянный луп включаем
asyncio.run(manager.watch_payments())

# result = asyncio.run(enricher.get_payments_by_intent(PaymentToProcess, payment_intent="test_intent2"))
# print(result)







