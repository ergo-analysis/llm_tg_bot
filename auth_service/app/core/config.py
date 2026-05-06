from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """Настройки приложения"""
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_prefix="",
        case_sensitive=False,)

    APP_NAME:str
    ENV:str

    JWT_SECRET: str
    JWT_ALG:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int

    SQLITE_PATH: str


settings=Settings()

def get_database_url() -> str:
    """Формирует URL для подключения к БД"""
    return f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"
