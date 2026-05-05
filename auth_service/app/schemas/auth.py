from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    """Запрос на регистрацию пользователя"""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Пароль не менее 6 символов")

class TokenResponse(BaseModel):
    """Ответ с валидныйм токеном"""
    access_token: str
    token_type: str = "bearer"