# backend/settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str | None = None

    class Config:
        env_file = "../.env"  # if you run from repo root; adjust path as needed

settings = Settings()
