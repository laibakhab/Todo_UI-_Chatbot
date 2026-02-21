from sqlmodel import create_engine, Session
from contextlib import contextmanager
from .config import settings
import os

# Create database engine
database_url = settings.database_url


def get_engine():
    """Create and return database engine."""
    # Add connection pool settings for PostgreSQL/Neon
    connect_args = {}
    if settings.database_url.startswith("postgresql"):
        # Configure for PostgreSQL/Neon
        connect_args = {
            "pool_pre_ping": True,  # Verify connections before use
            "pool_recycle": 300,    # Recycle connections every 5 minutes
        }

    return create_engine(
        settings.database_url,
        echo=False,
        **connect_args
    )


@contextmanager
def get_session():
    """Provide a transactional scope around a series of operations."""
    engine = get_engine()
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    """Dependency for FastAPI to get database session."""
    with get_session() as session:
        yield session