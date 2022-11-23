from celery import Celery
from celery.schedules import crontab
from src.core.config import redis_setting
from src.services.subscriptions import get_expiring_subscriptions

celery = Celery('tasks', broker=f'redis://{redis_setting.host}:{redis_setting.port}')


@celery.task
def send_notifications():
    """
    Предполагаем что есть ручка сервиса notifications для отправки уведомлений об окончании подписки
    """
    expiring_subscriptions = get_expiring_subscriptions()
    for row in expiring_subscriptions:
        print(f'send message to user {row.user_id} about date {row.end_date} for subscription {row.title}')
    return 'done!'


@celery.on_after_configure.connect
def setup_scheduler_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=12, minute=21),  # Время указывается по UTC
        send_notifications.s(),
        name='Send notifications about expiring subscriptions',
    )
