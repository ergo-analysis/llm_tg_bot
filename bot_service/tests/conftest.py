import pytest
from unittest.mock import AsyncMock, MagicMock
import fakeredis.aioredis


@pytest.fixture(autouse=True)
def mock_redis(monkeypatch, mocker):
    """Подменяет get_redis на fake Redis с decode_responses=True и мокает Celery backend."""
    fake_conn = fakeredis.aioredis.FakeRedis(decode_responses=True)
    async def fake_get_redis():
        return fake_conn
    monkeypatch.setattr("app.bot.handlers.get_redis", fake_get_redis)
    monkeypatch.setattr("app.infra.redis.get_redis", fake_get_redis)
    # Mock Celery backend to avoid Redis connection issues in tests
    mocker.patch("app.infra.celery_app.celery_app.backend.on_task_call")
    return fake_conn

@pytest.fixture
def mock_llm_delay(mocker):
    """Мокает send_task метод Celery app."""
    return mocker.patch("app.infra.celery_app.celery_app.send_task")

@pytest.fixture
def mock_bot(mocker):
    """Мокает Telegram Bot, чтобы избежать реальных вызовов API."""
    return mocker.patch("app.tasks.llm_tasks.Bot")

@pytest.fixture
def sample_jwt_token():
    """Создаёт тестовый JWT."""
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from app.core.config import settings

    payload = {
        "sub": "123",
        "role": "user",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

@pytest.fixture
def expired_jwt_token():
    """Создаёт истекший JWT токен."""
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from app.core.config import settings

    payload = {
        "sub": "123",
        "role": "user",
        "iat": datetime.now(timezone.utc) - timedelta(hours=2),
        "exp": datetime.now(timezone.utc) - timedelta(hours=1)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

@pytest.fixture
def token_missing_sub():
    """Создаёт JWT без поля sub."""
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from app.core.config import settings

    payload = {
        "role": "user",
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

@pytest.fixture
def mock_message():
    """Базовая заготовка сообщения Telegram."""
    msg = MagicMock()
    msg.from_user = MagicMock()
    msg.from_user.id = 123456789
    msg.text = ""
    msg.answer = AsyncMock()
    return msg
