
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import User

class UserRepository:
    """Репозиторий пользователей"""
    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_id(self, user_id: int) -> User | None:
        """Получение пользователя по id"""
        user = await self._db.get(User, user_id)
        return user 

    async def get_by_email(self, user_email: str) -> User | None:
        """Получение пользователя по email"""
        user = await self._db.scalar(select(User).where(User.email == user_email)) 
        return user 

    async def create(self, email, password_hash) -> User:
        """Создание нового пользователя"""
        user = User(
            email=email,
            password_hash=password_hash,
        )
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user
    