import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from src.tools.task_tools import add_task_tool

def test_task_tools():
    print("Testing task tools...")
    
    try:
        # Test adding a task
        result = add_task_tool(user_id="19", title="Test task from tool", description="Test description")
        print(f"Add task result: {result}")
        
        if "error" in result:
            print(f"Error occurred: {result['error']}")
        else:
            print("Task added successfully!")
            
    except Exception as e:
        print(f"Task tool test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_task_tools()