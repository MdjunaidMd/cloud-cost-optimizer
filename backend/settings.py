# backend/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str | None = None

    class Config:
        env_file = ".env"  # ✅ safer: Render sets vars, so this won’t matter in prod

settings = Settings()
