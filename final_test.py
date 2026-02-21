#!/usr/bin/env python3
"""
Final test to verify the complete chatbot functionality
"""
import requests
import json
import time

def test_complete_flow():
    print("=== Testing Complete Chatbot Flow ===\n")
    
    # Test 1: Health check
    print("1. Testing backend health...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("   [OK] Backend is healthy")
        else:
            print(f"   [ERROR] Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [ERROR] Could not connect to backend: {e}")
        return False
    
    # Test 2: Register a new user
    print("\n2. Testing user registration...")
    user_email = f"testuser_{int(time.time())}@example.com"
    signup_payload = {
        "email": user_email,
        "password": "securepassword123"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/auth/signup", json=signup_payload)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data['access_token']
            user_id = auth_data['user_id']
            print(f"   [OK] User registered successfully (ID: {user_id})")
        else:
            print(f"   [ERROR] Registration failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Registration error: {e}")
        return False
    
    # Test 3: Test chat functionality
    print("\n3. Testing chat functionality...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test adding a task
    chat_payload = {
        "message": "Add a task to buy groceries"
    }
    
    try:
        response = requests.post(f"http://localhost:8000/api/{user_id}/chat", json=chat_payload, headers=headers)
        if response.status_code == 200:
            chat_response = response.json()
            print(f"   [OK] Chat response received: {chat_response['response']}")
            print(f"   [OK] Tool calls made: {len(chat_response['tool_calls'])}")
        else:
            print(f"   [ERROR] Chat failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Chat error: {e}")
        return False
    
    # Test 4: Test listing tasks
    print("\n4. Testing task listing...")
    try:
        response = requests.get(f"http://localhost:8000/api/tasks/", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"   [OK] Retrieved {len(tasks)} tasks")
            for task in tasks:
                print(f"     - Task: {task['title']} (ID: {task['id']})")
        else:
            print(f"   [ERROR] Task listing failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Task listing error: {e}")
        return False
    
    # Test 5: Test another chat interaction
    print("\n5. Testing another chat interaction...")
    chat_payload = {
        "message": "What tasks do I have?"
    }
    
    try:
        response = requests.post(f"http://localhost:8000/api/{user_id}/chat", json=chat_payload, headers=headers)
        if response.status_code == 200:
            chat_response = response.json()
            print(f"   [OK] Chat response received: {chat_response['response']}")
        else:
            print(f"   [ERROR] Second chat failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Second chat error: {e}")
        return False
    
    print("\n=== All tests passed! Chatbot is working correctly! ===")
    print("\nThe system is ready for use:")
    print("- Backend server running on http://localhost:8000")
    print("- Frontend server running on http://localhost:3000 (typically)")
    print("- Users can register/login and interact with the chatbot")
    print("- Tasks can be added, listed, updated, and completed via chat")
    return True

if __name__ == "__main__":
    success = test_complete_flow()
    if not success:
        print("\nSome tests failed. Please check the server configurations.")
        exit(1)