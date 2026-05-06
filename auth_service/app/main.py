from fastapi import FastAPI
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
from .api.router import api_router
from .core.config import settings
from .db import Base, engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создает таблицы при запуске"""
    logger.info('connecting engine')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("disposing engine")
    await engine.dispose()


def create_app() -> FastAPI:
    """Фабрика приложения FastAPI"""
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    app.include_router(api_router)

    
    @app.get("/health")
    async def health():
        """Пингует сервер, проверяет работоспособность"""
        return {"status": "ok", "env": settings.ENV}
    
    return app

app = create_app()
