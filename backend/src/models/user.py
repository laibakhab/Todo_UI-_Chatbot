from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import hashlib
import secrets
from passlib.context import CryptContext


# CryptContext uses bcrypt for new hashes; existing SHA-256 legacy hashes handled in verify_password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a stored hash.

    Supports two formats:
    - bcrypt: starts with $2b$, $2a$, or $2y$
    - Legacy SHA-256: salt:sha256_hex_digest
    """
    try:
        if hashed_password.startswith(("$2b$", "$2a$", "$2y$")):
            # bcrypt format — use passlib
            return pwd_context.verify(plain_password, hashed_password)
        elif ":" in hashed_password:
            # Legacy format: "<salt>:<sha256_hex>"
            salt, stored_hash = hashed_password.split(":", 1)
            computed = hashlib.sha256((plain_password + salt).encode()).hexdigest()
            return computed == stored_hash
        else:
            return False
    except Exception:
        return False


class UserBase(SQLModel):
    """Base model for user with common fields."""
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    """User model representing an application user."""
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationship to Tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    # Relationship to Conversations # PHASE 3 ADDITION
    conversations: List["Conversation"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(min_length=8)


class UserRegister(SQLModel):
    """Schema for user registration."""
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=72)  # bcrypt limit


class UserLogin(SQLModel):
    """Schema for user login."""
    email: str = Field(max_length=255)
    password: str = Field(min_length=1, max_length=72)  # bcrypt limit


class UserPublic(UserBase):
    """Public schema for returning user data (without sensitive info)."""
    id: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, user):
        """Create UserPublic instance from User model."""
        return cls(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at
        )


class UserPublicFromToken(UserBase):
    """Public schema for JWT token-based user data (timestamps not available from token)."""
    id: int


class UserWithPassword(UserPublic):
    """Schema for returning user with password hash (internal use only)."""
    password_hash: str
