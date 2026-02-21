import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from src.db import get_engine
from sqlmodel import Session, select
from src.models import Conversation, Message, ConversationCreate, MessageCreate
from src.tools.task_tools import add_task_tool

def test_chat_endpoint_logic():
    print("Testing chat endpoint logic step by step...")
    
    try:
        # Create database engine and session
        engine = get_engine()
        
        with Session(engine) as db:
            print("1. Creating conversation...")
            # Create a new conversation
            conversation_data = ConversationCreate(title=None)
            conversation = Conversation(
                **conversation_data.model_dump(),
                user_id=23  # Use the user ID from our test
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            print(f"   Created conversation with ID: {conversation.id}")
            
            print("2. Creating user message...")
            # Create a user message
            message_data = MessageCreate(
                role="user",
                content="Add a task to buy groceries"
            )
            user_message = Message(
                **message_data.model_dump(exclude_unset=True),
                conversation_id=conversation.id
            )
            db.add(user_message)
            db.commit()
            print(f"   Created message with ID: {user_message.id}")
            
            print("3. Testing task tool call...")
            # Test the task tool call
            result = add_task_tool(
                user_id="23",
                title="buy groceries",
                description="Description for buy groceries"
            )
            print(f"   Task tool result: {result}")
            
            print("4. Creating assistant message...")
            # Create an assistant message
            assistant_message_data = MessageCreate(
                role="assistant",
                content="Task added: buy groceries"
            )
            assistant_message = Message(
                **assistant_message_data.model_dump(exclude_unset=True),
                conversation_id=conversation.id
            )
            db.add(assistant_message)
            db.commit()
            print(f"   Created assistant message with ID: {assistant_message.id}")
            
            print("5. Fetching messages from conversation...")
            # Fetch messages from the conversation
            message_statement = select(Message).where(
                Message.conversation_id == conversation.id
            ).order_by(Message.timestamp.asc())
            messages_history = db.exec(message_statement).all()
            print(f"   Retrieved {len(messages_history)} messages from conversation")
            
            # Clean up - remove test conversation and associated messages
            print("6. Cleaning up test data...")
            # First delete messages associated with the conversation
            for msg in messages_history:
                db.delete(msg)
            # Then delete the conversation
            db.delete(conversation)
            db.commit()
            print("   Cleanup completed")
            
        print("\nAll steps completed successfully!")
        
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_endpoint_logic()