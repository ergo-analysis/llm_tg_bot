from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import RegisterRequest, TokenResponse, UserPublic
from app.usecases.auth import AuthUseCase

from .deps import (
    get_auth_uc,
    get_current_user_id,  
)

router = APIRouter(prefix="/auth", tags=["auth"])

AuthUseCaseDep = Annotated[AuthUseCase, Depends(get_auth_uc)]
OAuthDep = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    auth_uc: AuthUseCaseDep,
) -> UserPublic:
    """Регистрация нового пользователя с email и паролем"""

    user = await auth_uc.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    data: OAuthDep,
    auth_uc: AuthUseCaseDep
) -> TokenResponse:
    """Логин по email и паролю, возвращает JWT токен"""

    token = await auth_uc.login(data.username, data.password)
    return token


@router.get("/me", response_model=UserPublic)
async def me(
    auth_usecase: AuthUseCaseDep,
    user_id: int = Depends(get_current_user_id),
) -> UserPublic:
    """Возвращает публичную информацию текущего пользователя"""

    user = await auth_usecase.me(user_id)
    return user

