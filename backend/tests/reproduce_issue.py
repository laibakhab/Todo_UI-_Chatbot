
import os
import sys
import json
from unittest.mock import MagicMock, patch

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from sqlmodel import SQLModel, create_engine, Session, select

# Import models to register them with SQLModel.metadata
from src.models import User, Task, Conversation, Message

# Debug: Check if models are registered
print("DEBUG: SQLModel.metadata.tables keys:", list(SQLModel.metadata.tables.keys()))

from sqlmodel.pool import StaticPool

# Setup in-memory DB for testing - Use StaticPool to share data across sessions
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
SQLModel.metadata.create_all(engine)

# Verify table creation immediately
with Session(engine) as session:
    try:
        session.exec(select(User)).first()
        print("DEBUG: User table exists.")
    except Exception as e:
        print(f"DEBUG: User table check failed: {e}")

from src.main import app
from src.db import get_session, get_engine as get_real_engine

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

# Mock User
def mock_get_current_user():
    # We need to make sure this user exists in the DB
    with Session(engine) as session:
        user = session.get(User, 1)
        if not user:
             user = User(id=1, username="testuser", email="test@example.com", password_hash="hash")
             session.add(user)
             session.commit()
             session.refresh(user)
        return user

from src.utils.token import get_current_user
app.dependency_overrides[get_current_user] = mock_get_current_user

from fastapi.testclient import TestClient
client = TestClient(app)

def test_chat_add_task():
    # Mock OpenAI
    with patch("openai.OpenAI") as MockOpenAI:
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        
        # Mock the first response from OpenAI (deciding to call the tool)
        mock_message = MagicMock()
        mock_message.content = None
        
        # Create function mock with explicit name attribute
        function_mock = MagicMock()
        function_mock.name = "add_task_tool"
        function_mock.arguments = json.dumps({
            "user_id": "1",
            "title": "Buy Verified Milk",
            "description": "2 cartons"
        })
        
        tool_call_mock = MagicMock(id="call_123")
        tool_call_mock.function = function_mock
        
        mock_message.tool_calls = [tool_call_mock]
        
        # Mock the second response (confirmation after tool execution)
        mock_second_message = MagicMock()
        mock_second_message.content = "I have added the task 'Buy Verified Milk' for you."
        mock_second_message.tool_calls = None
        
        # Setup the mock to return these responses in sequence
        mock_client.chat.completions.create.side_effect = [
            MagicMock(choices=[MagicMock(message=mock_message)]),
            MagicMock(choices=[MagicMock(message=mock_second_message)])
        ]

        # Make the request with patched get_engine for tools
        print("Sending request to /api/1/chat...")
        with patch("src.tools.task_tools.get_engine", return_value=engine):
             response = client.post("/api/1/chat", json={"message": "Add a task to buy verified milk"})
        
        # Verify Response
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.json()}")
        
        assert response.status_code == 200
        data = response.json()
        assert "I have added the task" in data["response"]
        
        # Verify System Prompt contains user_id
        call_args = mock_client.chat.completions.create.call_args_list[0]
        messages = call_args[1]['messages']
        system_prompt = messages[0]['content']
        print(f"System Prompt: {system_prompt}")
        assert "Current User ID: 1" in system_prompt

        # Verify Tool Output sent back to LLM
        if len(mock_client.chat.completions.create.call_args_list) > 1:
            second_call_args = mock_client.chat.completions.create.call_args_list[1]
            second_messages = second_call_args[1]['messages']
            # Find the tool message
            for msg in second_messages:
                if msg.get('role') == 'tool':
                    print(f"Tool Output Sent to LLM: {msg.get('content')}")
        else:
            print("WARNING: Second call to LLM (after tool execution) was not made!")

        # Verify Database
        with Session(engine) as session:
            task = session.get(Task, 1) # Assuming first task has ID 1
            print(f"Task in DB: {task}")
            assert task is not None
            assert task.title == "Buy Verified Milk"
            assert task.user_id == 1

if __name__ == "__main__":
    try:
        test_chat_add_task()
        print("VERIFICATION PASSED")
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
