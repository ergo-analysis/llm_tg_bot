from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError, JWTError

from .exceptions import InvalidTokenError, TokenExpiredError
from .config import settings

# контекст хеширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Хеширует пароль"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int, role: str, expires_minutes: int | None = None) -> str:
    """Создает JWT токен"""
    ttl_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
    to_encode = {
        'sub': str(user_id),
        'role': role,
        "exp": expire,
        "iat": datetime.now(timezone.utc)}

    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> dict:
    """Верифицирует JWT токен"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG]
        )
        return payload
    
    except ExpiredSignatureError as e:
        raise TokenExpiredError() from e

    except JWTError as e:
        raise InvalidTokenError() from e
    