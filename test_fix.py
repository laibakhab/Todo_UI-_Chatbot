import sys
sys.path.insert(0, 'D:/Todo_UI _Chatbot/backend')

# Test the chat endpoint directly by importing and calling it
from src.routers.chat import chat_endpoint
from src.models import User
from src.utils.token import UserPublicFromToken
from unittest.mock import Mock
from sqlmodel import Session

def test_chat_directly():
    print("Testing chat endpoint directly...")
    
    # Create mock objects
    mock_request = Mock()
    mock_request.message = "Add a task to buy groceries"
    mock_request.conversation_id = None
    
    mock_db = Mock(spec=Session)
    
    # Create a mock authenticated user
    mock_current_user = UserPublicFromToken(id=1, email="test@example.com")
    
    try:
        # Try to call the chat endpoint function directly
        result = chat_endpoint(
            user_id="1",
            request=mock_request,
            db=mock_db,
            current_user=mock_current_user
        )
        print(f"Success! Result: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chat_directly()