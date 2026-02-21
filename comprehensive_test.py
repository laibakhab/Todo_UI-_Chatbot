import requests
import json

# Test the chatbot functionality
BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return False

def register_and_login():
    """Register a test user and get JWT token"""
    import time
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

def test_chatbot_operations(token, user_id):
    """Test various chatbot operations with authentication"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    operations = [
        {"message": "Add a task to buy groceries", "operation": "add"},
        {"message": "Update task 1 to buy milk and bread", "operation": "update"},
        {"message": "Complete task 1", "operation": "complete"},
        {"message": "Delete task 1", "operation": "delete"},
        {"message": "Show my tasks", "operation": "list"}
    ]
    
    for op in operations:
        print(f"\nTesting {op['operation']} operation: {op['message']}")
        chat_payload = {
            "message": op["message"]
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_payload, headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {json.dumps(result, indent=2)[:200]}...")  # Truncate long responses
            else:
                print(f"Error: {response.status_code} - {response.text[:200]}...")  # Truncate long errors
        except Exception as e:
            print(f"Exception during {op['operation']}: {e}")

def main():
    print("Testing Chatbot Integration...")
    
    if not test_health():
        print("API is not running. Please start the backend server first.")
        return
    
    print("\nRegistering and logging in test user...")
    token, user_id = register_and_login()
    
    if not token:
        print("Failed to authenticate. Cannot test chatbot.")
        return
    
    print(f"\nTesting various chatbot operations for user ID: {user_id}...")
    test_chatbot_operations(token, user_id)
    
    print("\n[TEST COMPLETE] Chatbot operations tested.")
    print("Check the server logs for any detailed error messages if operations failed.")

if __name__ == "__main__":
    main()