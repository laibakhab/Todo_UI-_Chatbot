import os
from src.config import settings
from sqlmodel import SQLModel
from src.db import get_engine


def create_tables():
    """Create all database tables."""
    print(f"Using database URL: {settings.database_url[:100]}...")
    engine = get_engine()

    # Import all models to ensure they're registered with SQLModel
    from src.models.user import User, UserRegister, UserLogin, UserCreate, UserPublic, UserWithPassword
    from src.models.task import Task, TaskBase, TaskCreate, TaskUpdate, TaskPublic

    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()