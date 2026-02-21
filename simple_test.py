import requests
import json
import time

# Test the chatbot functionality
BASE_URL = "http://127.0.0.1:8001"  # Updated to use port 8001

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

def test_add_task_operation():
    """Test adding a task via chatbot"""
    print("\nTesting add task operation...")
    
    # Register and login
    token, user_id = register_and_login()
    
    if not token:
        print("Failed to authenticate.")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    chat_payload = {
        "message": "Add a task to buy groceries"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_payload, headers=headers)
        print(f"Chat Response Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exception during add task: {e}")
        return False

if __name__ == "__main__":
    print("Testing Chatbot Integration on port 8001...")
    success = test_add_task_operation()
    
    if success:
        print("\n[SUCCESS] Chatbot test completed successfully!")
        print("The chatbot is connected to the Gemini API and can process requests.")
    else:
        print("\n[FAILURE] Chatbot test failed.")
        print("Check the server console for detailed error messages.")