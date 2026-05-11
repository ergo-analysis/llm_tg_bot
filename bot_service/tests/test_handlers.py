import pytest
from unittest.mock import AsyncMock, MagicMock
from app.bot.handlers import cmd_token, handle_text

pytestmark = pytest.mark.asyncio

class TestTokenCommand:
    async def test_save_valid_token(self, mock_redis, sample_jwt_token):
        msg = MagicMock()
        msg.from_user = MagicMock(id=12345)
        msg.text = f"/token {sample_jwt_token}"
        msg.answer = AsyncMock()

        await cmd_token(msg)

        saved = await mock_redis.get("token:12345")
        assert saved == sample_jwt_token
        msg.answer.assert_called_with("Токен сохранён! Можете задавать вопросы.", parse_mode=None)

    async def test_missing_token_argument(self, mock_redis):
        msg = MagicMock()
        msg.from_user = MagicMock(id=12345)
        msg.text = "/token"
        msg.answer = AsyncMock()

        await cmd_token(msg)

        msg.answer.assert_called_with("Используйте: /token <ваш_JWT>", parse_mode=None)
        saved = await mock_redis.get("token:12345")
        assert saved is None

    async def test_expired_token_still_saved(self, mock_redis, expired_jwt_token):
        """команда /token не проверяет срок действия, токен сохраняется."""
        msg = MagicMock()
        msg.from_user = MagicMock(id=12345)
        msg.text = f"/token {expired_jwt_token}"
        msg.answer = AsyncMock()

        await cmd_token(msg)

        saved = await mock_redis.get("token:12345")
        assert saved == expired_jwt_token
        msg.answer.assert_called_with("Токен сохранён! Можете задавать вопросы.", parse_mode=None)


class TestTextHandling:
    async def test_no_token_shows_instruction(self, mock_redis):
        msg = MagicMock()
        msg.from_user = MagicMock(id=999)
        msg.text = "Как дела?"
        msg.answer = AsyncMock()

        await handle_text(msg)
        msg.answer.assert_called_with("Сначала отправьте токен командой /token <JWT>", parse_mode=None)

    async def test_invalid_token_shows_error(self, mock_redis):
        await mock_redis.set("token:777", "bad.token")
        msg = MagicMock()
        msg.from_user = MagicMock(id=777)
        msg.text = "Вопрос"
        msg.answer = AsyncMock()

        await handle_text(msg)
        msg.answer.assert_called_with(
            "Ваш токен недействителен. Получите новый в Auth Service.", parse_mode=None
        )

    async def test_expired_token_shows_error(self, mock_redis, expired_jwt_token):
        """Истекший токен также вызывает сообщение о недействительности."""
        await mock_redis.set("token:777", expired_jwt_token)
        msg = MagicMock()
        msg.from_user = MagicMock(id=777)
        msg.text = "Вопрос"
        msg.answer = AsyncMock()

        await handle_text(msg)
        msg.answer.assert_called_with(
            "Ваш токен недействителен. Получите новый в Auth Service.", parse_mode=None
        )

    async def test_valid_token_calls_celery(self, mock_redis, mock_llm_delay, sample_jwt_token):
        await mock_redis.set("token:777", sample_jwt_token)
        msg = MagicMock()
        msg.from_user = MagicMock(id=777)
        msg.chat = MagicMock(id=888)
        msg.text = "Привет, LLM!"
        msg.answer = AsyncMock()

        await handle_text(msg)

        mock_llm_delay.assert_called_once_with('llm_request', kwargs={'tg_chat_id': 888, 'prompt': 'Привет, LLM!'})
        msg.answer.assert_called_with("Запрос принят, ожидайте ответ...", parse_mode=None)
