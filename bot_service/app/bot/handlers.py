from aiogram import Router, types
from aiogram.filters import Command
from ..infra import get_redis
from ..core.jwt import decode_and_validate

router = Router()

@router.message(Command("token"))
async def cmd_token(message: types.Message):
    try:
        _, token = message.text.split(maxsplit=1)
    except ValueError:
        await message.answer("Используйте: /token <ваш_JWT>", parse_mode=None)
        return
    redis = await get_redis()
    user_id = message.from_user.id
    await redis.set(f"token:{user_id}", token)
    await message.answer("Токен сохранён! Можете задавать вопросы.", parse_mode=None)

@router.message()
async def handle_text(message: types.Message):
    redis = await get_redis()
    user_id = message.from_user.id
    token = await redis.get(f"token:{user_id}")
    if not token:
        await message.answer("Сначала отправьте токен командой /token <JWT>", parse_mode=None)
        return
    try:
        payload = decode_and_validate(token) # noqa: F841
    except ValueError:
        await message.answer("Ваш токен недействителен. Получите новый в Auth Service.", parse_mode=None)
        return

    from ..infra.celery_app import celery_app
    celery_app.send_task('llm_request', kwargs={'tg_chat_id': message.chat.id, 'prompt': message.text})
    await message.answer("Запрос принят, ожидайте ответ...", parse_mode=None)
