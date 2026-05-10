import os
os.environ["PYDANTIC_EMAIL_VALIDATOR_SKIP_MX_CHECK"] = "true"

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite://"

@pytest.fixture(autouse=True)
def patch_email_validator(monkeypatch):
    import email_validator
    def fake_validate_email(email, **kwargs):
        class FakeEmail:
            normalized = email
            local_part = email.split('@')[0]
            domain = email.split('@')[1]
        return FakeEmail()
    monkeypatch.setattr(email_validator, "validate_email", fake_validate_email)

@pytest.fixture(scope="function")
async def client(monkeypatch):
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

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    sess.engine = original_engine
    sess.SessionLocal = original_sessionmaker
    app.dependency_overrides.clear()
