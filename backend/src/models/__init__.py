from .user import User, UserCreate, UserRegister, UserLogin, UserPublic, UserWithPassword
from .task import Task, TaskCreate, TaskUpdate, TaskPublic
from .chat_models import Conversation, Message, ConversationCreate, ConversationPublic, MessageCreate, MessagePublic  # PHASE 3 ADDITION

__all__ = [
    "User",
    "UserCreate",
    "UserRegister",
    "UserLogin",
    "UserPublic",
    "UserWithPassword",
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskPublic",
    "Conversation",  # PHASE 3 ADDITION
    "Message",  # PHASE 3 ADDITION
    "ConversationCreate",  # PHASE 3 ADDITION
    "ConversationPublic",  # PHASE 3 ADDITION
    "MessageCreate",  # PHASE 3 ADDITION
    "MessagePublic"  # PHASE 3 ADDITION
]