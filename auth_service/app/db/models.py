from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"   
     
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, 
        index=True, autoincrement=True)
    
    email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
    
    password_hash: Mapped[str] = mapped_column(
        String(128), nullable=False)
    
    role: Mapped[str] = mapped_column(
        String(50), default="user", nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False)
