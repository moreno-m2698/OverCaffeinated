from pydantic_settings import BaseSettings
from functools import lru_cache

# This class must be kept up to date with the .env file
class Settings(BaseSettings):
    ENV: str = "development"
    DEV_DB_PATH: str = "mock.db"
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = "development.env"

@lru_cache()
def get_settings():
    return Settings()