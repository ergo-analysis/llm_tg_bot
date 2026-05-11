from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from app.core.config import settings
from app.bot.handlers import router
from ..infra.celery_app import ensure_celery_connection
import asyncio
import logging

logger = logging.getLogger(__name__)

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
dp.include_router(router)

async def start_polling():
    max_retries = 30
    for attempt in range(max_retries):
        if ensure_celery_connection():
            logger.info("bot.dispatcher  начал устанавливает соединение")
            await dp.start_polling(bot)
            break
        else:
            wait_time = min(2 ** attempt, 10) 
            logger.warning(f"Соединение с Celery упало. Повтор через: {wait_time}s (попытка: {attempt + 1}/{max_retries})")
            await asyncio.sleep(wait_time)
    else:
        logger.error("Ошибка соединения с Celery, превышено число попыток. Exit.")
        raise RuntimeError("Невозможно установить соединение с Celery")
