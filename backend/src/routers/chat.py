from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from ..db import get_db
from ..models import User, Conversation, Message, ConversationCreate, MessageCreate
from sqlalchemy.orm import Session
from datetime import datetime
from sqlmodel import select
from ..utils.token import get_current_user  # Using existing token utility
import os
import json
from openai import OpenAI
from ..config import settings
from ..tools.task_tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool

# Initialize OpenAI client
client = OpenAI(api_key=settings.openai_api_key)

# Define tools for OpenAI function calling
TASK_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task/todo for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the task"},
                    "description": {"type": "string", "description": "Optional description of the task"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks/todos for the user",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The ID of the task to complete"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The ID of the task to delete"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title, description, or completion status",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The ID of the task to update"},
                    "title": {"type": "string", "description": "New title for the task"},
                    "description": {"type": "string", "description": "New description for the task"},
                    "completed": {"type": "boolean", "description": "New completion status"}
                },
                "required": ["task_id"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are a helpful Todo task management assistant. You help users manage their tasks/todos.
You can add, list, complete, delete, and update tasks.
Be friendly and concise in your responses. When a user asks to add a task, extract the task title from their message.
Always confirm actions you take. If listing tasks, format them nicely."""


def execute_tool_call(tool_name: str, arguments: dict, user_id_str: str) -> dict:
    """Execute a tool call and return the result."""
    if tool_name == "add_task":
        return add_task_tool(user_id=user_id_str, title=arguments["title"], description=arguments.get("description"))
    elif tool_name == "list_tasks":
        return list_tasks_tool(user_id=user_id_str)
    elif tool_name == "complete_task":
        return complete_task_tool(user_id=user_id_str, task_id=arguments["task_id"])
    elif tool_name == "delete_task":
        return delete_task_tool(user_id=user_id_str, task_id=arguments["task_id"])
    elif tool_name == "update_task":
        return update_task_tool(
            user_id=user_id_str, task_id=arguments["task_id"],
            title=arguments.get("title"), description=arguments.get("description"),
            completed=arguments.get("completed")
        )
    return {"error": "Unknown tool"}


# Define request/response models for chat endpoint
class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[Dict[str, Any]]


# Create router for chat endpoint
router = APIRouter(tags=["chat"])  # No prefix since main.py uses /api as prefix


@router.post("/{user_id}/chat", response_model=ChatResponse)
def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Chat endpoint that handles conversation with AI.

    Args:
        user_id: The ID of the user having the conversation
        request: Contains conversation_id (optional) and message

    Returns:
        ChatResponse with conversation_id, response, and tool_calls
    """
    try:
        print(f"DEBUG: Chat endpoint called with user_id: {user_id}")
        print(f"DEBUG: Current user from token: {current_user.id}, email: {current_user.email}")

        # After successful authentication, we can trust the current_user
        # Verify the user_id in the path matches the authenticated user
        try:
            # Attempt to convert the path user_id to int for database comparison
            requested_user_id = int(user_id)
            if current_user.id != requested_user_id:
                print(f"DEBUG: Authorization failed - Token user: {current_user.id}, Requested: {requested_user_id}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not authorized to access this user's conversations. Token user: {current_user.id}, Requested: {requested_user_id}"
                )
            user_id_int = current_user.id  # Use the authenticated user's ID for database operations
        except ValueError:
            # If user_id is not numeric, we should compare with the authenticated user's email username
            # But the preferred approach is to use integer user IDs
            # For backward compatibility or special cases, we can check email
            user_email_username = current_user.email.split('@')[0] if current_user.email else ""
            if user_email_username != user_id:
                print(f"DEBUG: Authorization failed - Email username: {user_email_username}, Requested: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not authorized to access this user's conversations. Email username: {user_email_username}, Requested: {user_id}"
                )
            # Use the authenticated user's actual ID for database operations
            user_id_int = current_user.id

        print(f"DEBUG: Authorized user_id_int: {user_id_int}")

        # Cast user_id to string for DB queries (DB column is varchar)
        user_id_str = str(user_id_int)

        # Get or create conversation
        conversation = None
        if request.conversation_id:
            try:
                # Try to find existing conversation
                conversation_id_int = int(request.conversation_id)
                statement = select(Conversation).where(
                    Conversation.id == conversation_id_int,
                    Conversation.user_id == user_id_str
                )
                conversation_result = db.exec(statement).first()

                if not conversation_result:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Conversation not found"
                    )
                conversation = conversation_result
            except ValueError:
                # Invalid integer format
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid conversation ID format"
                )
        else:
            # Create new conversation
            print("DEBUG: Creating new conversation")
            conversation_data = ConversationCreate(title="New Conversation")  # Provide a default title
            conversation = Conversation(
                **conversation_data.model_dump(),  # Use model_dump() instead of dict()
                user_id=user_id_str
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            print(f"DEBUG: Created conversation with ID: {conversation.id}")

        # Fetch history: Get all Messages for conversation_id (ordered by created_at)
        message_statement = select(Message).where(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.asc())
        messages_history = db.exec(message_statement).all()
        print(f"DEBUG: Found {len(messages_history)} existing messages")

        # Build messages array for agent: [history messages + new user message]
        formatted_messages = []
        for msg in messages_history:
            formatted_messages.append({"role": msg.role, "content": msg.content})

        # Add the new user message to the messages array
        formatted_messages.append({"role": "user", "content": request.message})

        # Store new user Message in DB (user_id, conversation_id, role="user", content=message, created_at)
        message_data = MessageCreate(
            role="user",
            content=request.message
        )
        user_message = Message(
            **message_data.model_dump(exclude_unset=True),  # Use model_dump() instead of dict()
            conversation_id=conversation.id,
            user_id=user_id_str  # Added user_id
        )
        db.add(user_message)
        db.commit()
        print("DEBUG: Stored user message in DB")

        # Call OpenAI API with function calling
        print(f"DEBUG: Processing message with OpenAI: {request.message}")
        final_tool_calls = []
        try:
            # Add system prompt at the beginning
            openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + formatted_messages

            # First OpenAI call
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=openai_messages,
                tools=TASK_TOOLS,
                tool_choice="auto"
            )

            assistant_msg = response.choices[0].message

            # Check if OpenAI wants to call tools
            if assistant_msg.tool_calls:
                # Add assistant message with tool calls to conversation
                openai_messages.append(assistant_msg)

                for tool_call in assistant_msg.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    print(f"DEBUG: OpenAI tool call: {func_name}({func_args})")

                    # Execute the tool
                    tool_result = execute_tool_call(func_name, func_args, user_id_str)
                    print(f"DEBUG: Tool result: {tool_result}")

                    final_tool_calls.append({
                        "name": func_name,
                        "arguments": func_args
                    })

                    # Add tool result to messages
                    openai_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })

                # Second OpenAI call to get final response after tool execution
                second_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=openai_messages
                )
                ai_response_content = second_response.choices[0].message.content
            else:
                # No tool calls, just use the response directly
                ai_response_content = assistant_msg.content

        except Exception as e:
            print(f"Error calling OpenAI: {str(e)}")
            import traceback
            traceback.print_exc()
            ai_response_content = "I'm sorry, I encountered an error processing your request. Please try again."
            final_tool_calls = []

        # Store assistant Message in DB (role="assistant", content=response)
        assistant_message_data = MessageCreate(
            role="assistant",
            content=ai_response_content
        )
        assistant_message = Message(
            **assistant_message_data.model_dump(exclude_unset=True),  # Use model_dump() instead of dict()
            conversation_id=conversation.id,
            user_id=user_id_str  # Added user_id
        )
        db.add(assistant_message)
        db.commit()
        print("DEBUG: Stored assistant message in DB")

        # Return: {"conversation_id": int, "response": str, "tool_calls": array}
        print(f"DEBUG: Returning response with conversation_id: {conversation.id}")
        return ChatResponse(
            conversation_id=str(conversation.id),
            response=ai_response_content,
            tool_calls=final_tool_calls
        )
    except Exception as e:
        print(f"ERROR in chat_endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


# Additional endpoints for managing conversations

@router.get("/{user_id}/conversations")
def get_user_conversations(
    user_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all conversations for a user
    """
    try:
        # Attempt to convert the path user_id to int for database comparison
        requested_user_id = int(user_id)
        if current_user.id != requested_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to access this user's conversations. Token user: {current_user.id}, Requested: {requested_user_id}"
            )
        user_id_int = requested_user_id
    except ValueError:
        # If user_id is not numeric, we should compare with the authenticated user's email username
        user_email_username = current_user.email.split('@')[0] if current_user.email else ""
        if user_email_username != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to access this user's conversations. Email username: {user_email_username}, Requested: {user_id}"
            )
        # Use the authenticated user's actual ID for database operations
        user_id_int = current_user.id

    statement = select(Conversation).where(
        Conversation.user_id == str(user_id_int)
    ).order_by(Conversation.updated_at.desc())
    conversations = db.exec(statement).all()

    return conversations


@router.get("/{user_id}/conversations/{conversation_id}/messages")
def get_conversation_messages(
    user_id: str,
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all messages for a specific conversation
    """
    try:
        # Attempt to convert the path user_id to int for database comparison
        requested_user_id = int(user_id)
        if current_user.id != requested_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to access this user's conversations. Token user: {current_user.id}, Requested: {requested_user_id}"
            )
        user_id_int = requested_user_id
    except ValueError:
        # If user_id is not numeric, we should compare with the authenticated user's email username
        user_email_username = current_user.email.split('@')[0] if current_user.email else ""
        if user_email_username != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not authorized to access this user's conversations. Email username: {user_email_username}, Requested: {user_id}"
            )
        # Use the authenticated user's actual ID for database operations
        user_id_int = current_user.id

    try:
        conversation_id_int = int(conversation_id)
        statement = select(Conversation).where(
            Conversation.id == conversation_id_int,
            Conversation.user_id == str(user_id_int)
        )
        conversation_result = db.exec(statement).first()

        if not conversation_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        conversation = conversation_result
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )

    message_statement = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at.asc())
    messages = db.exec(message_statement).all()

    return messages