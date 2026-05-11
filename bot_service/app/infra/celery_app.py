from celery import Celery
from app.core.config import settings

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
    broker_transport_options={
        'max_retries': 10,
        'interval_start': 2,
        'interval_step': 2,
        'interval_max': 10,
    },
)

import app.tasks.llm_tasks  # noqa: F401
