from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from functools import lru_cache


ENV = os.getenv("ENV")

class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}" if ENV else None,
        case_sensitive=False
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

