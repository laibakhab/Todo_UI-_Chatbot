import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from src.db import get_engine
from sqlmodel import Session, select
from src.models import Conversation, Message, ConversationCreate, MessageCreate

def test_conversation_creation():
    print("Testing conversation creation...")
    
    try:
        # Create database engine and session
        engine = get_engine()
        
        with Session(engine) as db:
            print("Creating conversation with title 'New Conversation'...")
            # Create a new conversation with a proper title
            conversation_data = ConversationCreate(title="New Conversation")
            conversation = Conversation(
                **conversation_data.model_dump(),
                user_id=24  # Use the user ID from our test
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            print(f"Created conversation with ID: {conversation.id}, title: '{conversation.title}'")
            
            # Clean up
            db.delete(conversation)
            db.commit()
            print("Cleaned up test conversation")
            
        print("Conversation creation test passed!")
        
    except Exception as e:
        print(f"Error in conversation creation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_conversation_creation()