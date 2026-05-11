from jose.exceptions import ExpiredSignatureError, JWTError

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from ..db import get_db as _get_db
from ..repositories import UserRepository
from ..usecases import AuthUseCase
from ..core import decode_token, InvalidTokenError, TokenExpiredError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """реализация Dependency сессии по тз"""
    async for session in _get_db():
        yield session


async def get_users_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Получает репозиторий из сессии"""
    return UserRepository(db)


async def get_auth_uc(storage: UserRepository = Depends(get_users_repo)) -> AuthUseCase:
    """Получает usecase аутентификации"""
    return AuthUseCase(storage)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Получает ID текущего пользователя из JWT токена"""
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError()
        return user_id

    except ExpiredSignatureError:
        raise TokenExpiredError()
    
    except JWTError:
        raise InvalidTokenError()
    