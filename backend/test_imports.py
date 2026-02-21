# Test the Gemini API integration directly
import os
from src.config import settings

print("Checking settings...")
print(f"Gemini API Key in settings: {'Yes' if settings.gemini_api_key else 'No'}")
print(f"Gemini API Key in env: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")

# Test importing the chat functionality
try:
    from src.routers.chat import chat_endpoint
    print("Chat endpoint imported successfully")
except Exception as e:
    print(f"Error importing chat endpoint: {e}")
    import traceback
    traceback.print_exc()

# Test the tools
try:
    from src.tools.task_tools import add_task_tool
    print("Task tools imported successfully")
except Exception as e:
    print(f"Error importing task tools: {e}")
    import traceback
    traceback.print_exc()