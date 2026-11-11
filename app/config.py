from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Microservice Boilerplate"
    APP_VERSION: str = "0.1.0"
    APP_ENV: Literal["local", "staging", "production"] = "local"
    APP_DEBUG: bool = True
    APP_KEY: SecretStr

    DATABASE_URL: str
    REDIS_URL: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
        env_ignore_empty=True,
    )


settings = Settings()
