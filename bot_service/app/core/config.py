from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """Настройки bot_service"""
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_prefix="",
        case_sensitive=False,)
    
    APP_NAME: str 
    ENV: str 
    TELEGRAM_BOT_TOKEN: str
    JWT_SECRET: str
    JWT_ALG: str 
    REDIS_URL: str 
    RABBITMQ_URL: str 
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str 
    OPENROUTER_MODEL: str 
    OPENROUTER_SITE_URL: str 
    OPENROUTER_APP_NAME: str 

settings = Settings()
