from celery import shared_task
from app.infra.celery_app import celery_app
from app.services.openrouter_client import openrouter_client
from aiogram import Bot
from app.core.config import settings

@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str):
    """Задача Celery для обработки LLM-запроса"""
    import asyncio
    
    async def _run():
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        try:
            client = openrouter_client
            messages = [{"role": "user", "content": prompt}]
            answer = await client.chat_completion(messages)
            await bot.send_message(tg_chat_id, answer)
        except Exception as e:
            await bot.send_message(tg_chat_id, f"Ошибка: {str(e)}")
        finally:
            await bot.session.close()
    
    asyncio.get_event_loop().run_until_complete(_run())
