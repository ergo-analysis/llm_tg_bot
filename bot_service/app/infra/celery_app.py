from celery import Celery
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    "bot_service",
    broker=settings.RABBITMQ_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=10,
    broker_heartbeat=0,
    broker_pool_limit=10,
    broker_transport_options={
        'max_retries': 20,
        'interval_start': 1,
        'interval_step': 0.5,
        'interval_max': 5,
        'visibility_timeout': 3600,
    },
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
)

import app.tasks.llm_tasks  # noqa: F401, E402


def ensure_celery_connection():
    """Проверка для коннекта к брокеру до тсарта бота"""
    try:
        with celery_app.connection() as conn:
            conn.connect()
        logger.info("Celery broker connection successful")
        return True
    except Exception as e:
        logger.error(f"Celery broker connection failed: {e}")
        return False
