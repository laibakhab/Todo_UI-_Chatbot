from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from sqlalchemy import JSON

if TYPE_CHECKING:
    from .user import User
    from .task import Task


class ConversationBase(SQLModel):
    """Base model for conversation with common fields."""
    title: str = Field(max_length=200)  # Changed from Optional[str] = Field(default=None, max_length=200) to str


class Conversation(ConversationBase, table=True):
    """Conversation model representing a chat conversation."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="conversations")

    # Relationship to Messages # PHASE 3 ADDITION
    messages: Optional[List["Message"]] = Relationship(back_populates="conversation")


class MessageBase(SQLModel):
    """Base model for message with common fields."""
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(max_length=5000)


class Message(MessageBase, table=True):
    """Message model representing a chat message."""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)  # Added user_id field
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Changed from timestamp to created_at to match DB

    # Relationship to Conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation."""
    pass


class ConversationPublic(ConversationBase):
    """Public schema for returning conversation data."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class MessageCreate(MessageBase):
    """Schema for creating a new message."""
    pass


class MessagePublic(MessageBase):
    """Public schema for returning message data."""
    id: int
    conversation_id: int
    user_id: int  # Added user_id field
    created_at: datetime  # Changed from timestamp to created_at to match DB