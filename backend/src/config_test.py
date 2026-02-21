from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    database_url: str = f"sqlite:///./test_todo_app.db"  # Use SQLite for testing

    # JWT settings
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Better Auth settings
    better_auth_secret: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()