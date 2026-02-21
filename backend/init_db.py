from sqlmodel import Session, create_engine
from src.models.user import User
from src.models.task import Task
from src.config import settings
from src.db import get_engine
from sqlalchemy import inspect


def init_db():
    """Initialize the database and create tables."""
    engine = get_engine()

    # Check if tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # Create tables if they don't exist
    if not tables:
        print("Creating database tables...")
        from src.models.user import User  # Import here to ensure models are registered
        from src.models.task import Task

        # Import all models to register them with SQLModel
        from src.models.user import User, UserRegister, UserLogin, UserCreate, UserPublic, UserWithPassword
        from src.models.task import Task, TaskBase, TaskCreate, TaskUpdate, TaskPublic

        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
    else:
        print(f"Database already initialized with tables: {tables}")


if __name__ == "__main__":
    init_db()