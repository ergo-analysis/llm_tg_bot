from ..core import (
    UserAlreadyExistsError,
    InvalidCredentialsError,   
    UserNotFoundError,
    hash_password,
    verify_password,
    create_access_token,
)

from ..repositories import UserRepository
from ..schemas import RegisterRequest, TokenResponse, UserPublic
from ..db import User

class AuthUseCase:
    """Логика аутентификации"""
    def __init__(self, storage: UserRepository) -> None:
        self._storage = storage


    def _public_response(self, data: User) -> UserPublic:
        return UserPublic.model_validate(data)


    async def register(self, data: RegisterRequest) -> UserPublic:
        """Регистрация"""
        occupied = await self._storage.get_by_email(data.email)
        if occupied:
            raise UserAlreadyExistsError()

        hashed = hash_password(data.password)
        user = await self._storage.create(data.email, hashed)
        return self._public_response(user)


    async def login(self, username: str, password: str) -> TokenResponse:
        user = await self._storage.get_by_email(username)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()   # вместо PermissionDeniedError()
        token = create_access_token(user.id, user.role)
        return TokenResponse(access_token=token)


    async def me(self, user_id: int) -> UserPublic:
        """Возвращает публичную схему пользователя"""
        user = await self._storage.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return self._public_response(user)
    