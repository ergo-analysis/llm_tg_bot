from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import get_database_url

class Database:
    """Класс подключения к БД"""
    def __init__(self, url: str | None = None):
        self.url = url or self._build_url()

        self.engine = create_async_engine(
            self.url,
            #echo=settings.APP_DEBUG,  
            future=True,)

        self.SessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False)

    def _build_url(self):
        return get_database_url()
    
    def get_session(self):
        return self.SessionLocal()

db = Database()
engine = db.engine
SessionLocal = db.SessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Генератор сессий"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
