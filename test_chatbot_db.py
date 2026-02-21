import requests
import json
import time

# Test the chatbot functionality
BASE_URL = "http://127.0.0.1:8000"

def register_and_login():
    """Register a test user and get JWT token"""
    # Use a unique email for each test run
    unique_email = f"test_{int(time.time())}@example.com"
    
    try:
        # Register a test user
        register_payload = {
            "email": unique_email,
            "password": "testpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/signup", json=register_payload)
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 200:
            print("User registered successfully")
        else:
            print(f"Registration failed: {response.text}")
            
        # Login to get JWT token
        login_payload = {
            "email": unique_email,
            "password": "testpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/signin", json=login_payload)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            user_id = result.get("user_id")
            print(f"Login successful, got token for user ID: {user_id}")
            return token, user_id
        else:
            print(f"Login failed: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"Error during authentication: {e}")
        return None, None

def test_add_task_via_chatbot(token, user_id):
    """Test adding a task via the chatbot"""
    print(f"\nTesting adding task via chatbot for user ID: {user_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test adding a task
    chat_payload = {
        "message": "Add a task to buy groceries"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_payload, headers=headers)
        print(f"Chat Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {json.dumps(result, indent=2)}")
            
            # Check if the tool call was made to add a task
            tool_calls = result.get("tool_calls", [])
            if tool_calls:
                print(f"Tool calls made: {len(tool_calls)}")
                for call in tool_calls:
                    print(f"- {call['name']}: {call['arguments']}")
            else:
                print("No tool calls were made")
                
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exception during add task: {e}")
        return False

def test_list_tasks(token, user_id):
    """Test listing tasks to verify the task was added"""
    print(f"\nTesting listing tasks for user ID: {user_id}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)
        print(f"List Tasks Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Tasks: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exception during list tasks: {e}")
        return False

def main():
    print("Testing Chatbot Integration with Neon Database...")
    
    # Register and login
    token, user_id = register_and_login()
    
    if not token:
        print("Failed to authenticate. Cannot test chatbot.")
        return
    
    # Test adding a task via chatbot
    success = test_add_task_via_chatbot(token, user_id)
    
    if success:
        print("\n[SUCCESS] Chatbot task addition test completed!")
        print("Now testing if the task was added to the database...")
        
        # Wait a moment for the task to be processed
        time.sleep(1)
        
        # Test listing tasks to verify it was added
        list_success = test_list_tasks(token, user_id)
        
        if list_success:
            print("\n[SUCCESS] Task was successfully added to the database!")
        else:
            print("\n[FAILURE] Could not verify task was added to the database.")
    else:
        print("\n[FAILURE] Chatbot task addition test failed.")

if __name__ == "__main__":
    main()