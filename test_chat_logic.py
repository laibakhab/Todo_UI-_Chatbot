import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from src.tools.task_tools import add_task_tool

def test_chat_logic():
    print("Testing chat logic...")
    
    # Simulate the logic from the chat endpoint
    message = "Add a task to buy groceries"
    message_lower = message.lower()
    
    print(f"Original message: {message}")
    print(f"Lowercase message: {message_lower}")
    
    if "add" in message_lower and "task" in message_lower:
        print("Detected add task command")
        
        # Extract task title from the message
        import re
        match = re.search(r"(?:to|for)\s+(.+)", message.lower())
        task_title = match.group(1) if match else "New task"
        
        print(f"Extracted task title: {task_title}")
        
        # Call the actual tool to add the task to the database
        result = add_task_tool(
            user_id="19",
            title=task_title,
            description=f"Description for {task_title}"
        )
        
        print(f"Tool result: {result}")
        
        ai_response_content = f"Task added: {task_title}"
        final_tool_calls = [{
            "name": "add_task_tool",
            "arguments": {
                "user_id": "19",
                "title": task_title,
                "description": f"Description for {task_title}"
            }
        }]
        
        print(f"Response content: {ai_response_content}")
        print(f"Tool calls: {final_tool_calls}")
        
    else:
        print("Did not detect add task command")

if __name__ == "__main__":
    test_chat_logic()