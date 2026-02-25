#!/usr/bin/env python3
"""
Test script to specifically test the chatbot functionality
"""
import requests
import json
import time

def test_chat_functionality():
    """Test the chatbot functionality."""
    print("Testing chatbot functionality...\n")
    
    # First, register a test user
    print("1. Registering test user...")
    signup_payload = {
        "email": f"chat_test_user_{int(time.time())}@example.com",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post("https://laibaasif-chatbot.hf.space/api/auth/signup", json=signup_payload)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data['access_token']
            user_id = auth_data['user_id']
            print(f"   User registered successfully. User ID: {user_id}")
        else:
            print(f"   Failed to register user: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   Error registering user: {str(e)}")
        return False
    
    # Test the chat endpoint
    print("\n2. Testing chat endpoint...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Send a test message to add a task
    chat_payload = {
        "message": "Add a task to buy groceries"
    }
    
    try:
        response = requests.post(f"https://laibaasif-chatbot.hf.space/api/{user_id}/chat", json=chat_payload, headers=headers)
        if response.status_code == 200:
            chat_response = response.json()
            print(f"   Chat response: {chat_response['response']}")
            print(f"   Tool calls: {len(chat_response['tool_calls'])} calls made")
        else:
            print(f"   Chat endpoint failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   Error calling chat endpoint: {str(e)}")
        return False
    
    # Test listing tasks
    print("\n3. Testing task listing...")
    try:
        response = requests.get(f"https://laibaasif-chatbot.hf.space/api/tasks/", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"   Found {len(tasks)} tasks")
            for task in tasks:
                print(f"     - {task['title']} (ID: {task['id']}, Completed: {task['completed']})")
        else:
            print(f"   Task listing failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   Error listing tasks: {str(e)}")
        return False
    
    # Test another chat message to list tasks
    print("\n4. Testing chat to list tasks...")
    chat_payload = {
        "message": "What tasks do I have?"
    }
    
    try:
        response = requests.post(f"https://laibaasif-chatbot.hf.space/api/{user_id}/chat", json=chat_payload, headers=headers)
        if response.status_code == 200:
            chat_response = response.json()
            print(f"   Chat response: {chat_response['response']}")
            print(f"   Tool calls: {len(chat_response['tool_calls'])} calls made")
        else:
            print(f"   Chat endpoint failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   Error calling chat endpoint: {str(e)}")
        return False
    
    print("\n[SUCCESS] Chatbot functionality test completed successfully!")
    return True

def main():
    success = test_chat_functionality()
    
    if success:
        print("\nChatbot is working correctly! You can:")
        print("- Interact with it through the frontend at http://localhost:3000")
        print("- Use the API directly with authenticated requests")
        print("- Add, list, update, and complete tasks through the chat interface")
    else:
        print("\n[FAILURE] Chatbot functionality test failed.")

if __name__ == "__main__":
    main()