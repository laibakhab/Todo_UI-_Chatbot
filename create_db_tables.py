import sys
import os

# Change to the backend directory to load .env properly
current_dir = os.path.dirname(__file__)
backend_dir = os.path.join(current_dir, 'backend')
os.chdir(backend_dir)

# Import settings first to ensure environment variables are loaded
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
    from src.models.chat_models import Conversation, Message, ConversationCreate, ConversationPublic, MessageCreate, MessagePublic

    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()