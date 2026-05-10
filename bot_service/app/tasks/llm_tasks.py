from celery import shared_task
from app.services.openrouter_client import OpenRouterClient
from aiogram import Bot
from app.core.config import settings

@shared_task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str):
    import asyncio
    async def _run():
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        try:
            client = OpenRouterClient()
            messages = [{"role": "user", "content": prompt}]
            answer = await client.chat_completion(messages)
            await bot.send_message(tg_chat_id, answer)
        except Exception as e:
            await bot.send_message(tg_chat_id, f"Ошибка: {str(e)}")
        finally:
            await bot.session.close()
    asyncio.get_event_loop().run_until_complete(_run())