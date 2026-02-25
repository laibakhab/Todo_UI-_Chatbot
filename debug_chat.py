import requests
import json
import time

# Register a test user
signup_payload = {
    "email": f"debug_user_{int(time.time())}@example.com",
    "password": "securepassword123"
}

response = requests.post("https://laibaasif-chatbot.hf.space/api/auth/signup", json=signup_payload)
if response.status_code == 200:
    auth_data = response.json()
    token = auth_data['access_token']
    user_id = auth_data['user_id']
    print(f"User registered. ID: {user_id}, Token: {token[:20]}...")

    # Try the chat endpoint with detailed error reporting
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    chat_payload = {
        "message": "Add a task to buy groceries"
    }
    
    print(f"Calling chat endpoint with user_id: {user_id}")
    response = requests.post(f"https://laibaasif-chatbot.hf.space/api/{user_id}/chat", json=chat_payload, headers=headers)
    print(f"Response status: {response.status_code}")
    print(f"Response text: {response.text}")
else:
    print(f"Failed to register user: {response.status_code}, {response.text}")