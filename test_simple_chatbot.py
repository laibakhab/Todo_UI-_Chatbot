import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

import requests
import time

def test_chatbot_functionality():
    """Test the chatbot functionality"""
    print("Testing chatbot functionality...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            print("✓ Server is running")
        else:
            print(f"✗ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Server is not accessible: {e}")
        return False
    
    # Test 2: Register a new user
    email = f"test_{int(time.time())}@example.com"
    password = "password123"
    
    try:
        register_resp = requests.post("http://127.0.0.1:8000/api/auth/signup", json={
            "email": email,
            "password": password
        }, timeout=10)
        
        if register_resp.status_code == 200:
            print("✓ User registration successful")
        else:
            print(f"✗ User registration failed: {register_resp.status_code}, {register_resp.text}")
            return False
    except Exception as e:
        print(f"✗ Registration request failed: {e}")
        return False
    
    # Test 3: Login to get token
    try:
        login_resp = requests.post("http://127.0.0.1:8000/api/auth/signin", json={
            "email": email,
            "password": password
        }, timeout=10)
        
        if login_resp.status_code == 200:
            login_data = login_resp.json()
            user_id = login_data.get("user_id")
            token = login_data.get("access_token")
            print(f"✓ Login successful, user_id: {user_id}")
        else:
            print(f"✗ Login failed: {login_resp.status_code}, {login_resp.text}")
            return False
    except Exception as e:
        print(f"✗ Login request failed: {e}")
        return False
    
    # Test 4: Test chat functionality to add a task
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        chat_resp = requests.post(f"http://127.0.0.1:8000/api/{user_id}/chat", json={
            "message": "Add a task to buy groceries"
        }, headers=headers, timeout=10)
        
        if chat_resp.status_code == 200:
            chat_data = chat_resp.json()
            print(f"✓ Chat response successful: {chat_data['response']}")
            print(f"  Conversation ID: {chat_data['conversation_id']}")
            print(f"  Tool calls: {len(chat_data['tool_calls'])}")
            return True
        else:
            print(f"✗ Chat request failed: {chat_resp.status_code}, {chat_resp.text}")
            return False
    except Exception as e:
        print(f"✗ Chat request failed: {e}")
        return False

def main():
    print("Make sure the server is running on http://127.0.0.1:8000 before running this test.")
    success = test_chatbot_functionality()
    
    if success:
        print("\n✓ All tests passed! The chatbot is working correctly.")
    else:
        print("\n✗ Some tests failed. The chatbot may not be working properly.")

if __name__ == "__main__":
    main()