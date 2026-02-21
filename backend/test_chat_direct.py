from src.routers.chat import chat_endpoint
from src.db import get_db
from src.models import User, Conversation, Message, ConversationCreate, MessageCreate
from src.utils.token import get_current_user
from fastapi import HTTPException
from unittest.mock import Mock
import sys
import os
sys.path.append(os.path.join(os.getcwd()))

def test_chat_function_directly():
    print("Testing chat function directly...")
    
    # Create mock objects
    mock_request = Mock()
    mock_request.message = "Add a task to buy groceries"
    mock_request.conversation_id = None
    
    # Mock user
    mock_current_user = Mock()
    mock_current_user.id = 1
    mock_current_user.email = "test@example.com"
    
    # Mock db session
    mock_db = Mock()
    
    # Mock the select query result
    mock_conversation = Mock()
    mock_conversation.id = 1
    mock_conversation.user_id = 1
    
    # Setup mock db.exec to return our mock objects
    mock_db.exec.return_value.first.return_value = mock_conversation
    mock_db.exec.return_value.all.return_value = []
    
    try:
        # Try calling the function directly with mocked dependencies
        result = chat_endpoint(
            user_id="1",
            request=mock_request,
            db=mock_db,
            current_user=mock_current_user
        )
        print("Function executed successfully:", result)
    except Exception as e:
        print(f"Error in function: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_function_directly()