import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite://"

@pytest.fixture(autouse=True, scope="function")
async def setup_db():
    """
    Создаёт in‑memory БД, переопределяет зависимость get_db,
    подменяет engine в app.db.session для корректной работы lifespan,
    удаляет таблицы после теста
    """

    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    test_sessionmaker = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    import app.db.session as sess
    original_engine = sess.engine
    original_sessionmaker = sess.SessionLocal
    sess.engine = test_engine
    sess.SessionLocal = test_sessionmaker

    async def override_get_db():
        async with test_sessionmaker() as session:
            yield session
    app.dependency_overrides[get_db] = override_get_db

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    sess.engine = original_engine
    sess.SessionLocal = original_sessionmaker
    app.dependency_overrides.clear()
    await test_engine.dispose()


@pytest.fixture
async def client():
    """HTTP-клиент для тестирования API."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user(client):
    """Регистрирует тестового пользователя и возвращает креды."""
    resp = await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert resp.status_code == 201
    return resp.json()
