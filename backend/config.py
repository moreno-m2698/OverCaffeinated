from pydantic_settings import BaseSettings
from functools import lru_cache

# This class must be kept up to date with the .env file
class Settings(BaseSettings):
    ENV: str = "development"
    DEV_DB_PATH: str = "mock.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = "development.env"

@lru_cache()
def get_settings():
    return Settings()