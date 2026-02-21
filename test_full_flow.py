import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from src.db import get_engine
from sqlmodel import Session
from src.utils.token import get_current_user
from src.models import Conversation, Message, MessageCreate

def test_chat_functionality():
    print("Testing chat functionality step by step...")
    
    try:
        # Test getting a database session
        print("Getting database engine...")
        engine = get_engine()
        print("Database engine acquired successfully")
        
        # Use the session within a context manager
        with Session(engine) as db:
            # Test creating a conversation
            print("Creating conversation...")
            from src.models import ConversationCreate
            conversation_data = ConversationCreate(title=None)
            conversation = Conversation(
                **conversation_data.dict(),
                user_id=20
            )
            print("Conversation object created")
            
            # Add to session
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            print(f"Conversation added to DB with ID: {conversation.id}")
            
            # Test creating a message
            print("Creating message...")
            message_data = MessageCreate(
                role="user",
                content="Add a task to buy groceries"
            )
            user_message = Message(
                **message_data.dict(exclude_unset=True),
                conversation_id=conversation.id
            )
            print("Message object created")
            
            # Add message to session
            db.add(user_message)
            db.commit()
            print("Message added to DB")
            
            # Test calling the task tool
            print("Testing task tool...")
            from src.tools.task_tools import add_task_tool
            result = add_task_tool(
                user_id="20",
                title="buy groceries",
                description="Description for buy groceries"
            )
            print(f"Task tool result: {result}")
            
            # Clean up - remove the test conversation
            db.delete(conversation)
            db.commit()
            print("Cleanup completed")
        
        print("All tests passed!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_functionality()