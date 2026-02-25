import subprocess
import time
import requests
import json
import threading

def run_server():
    import uvicorn
    from backend.src.main import app
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_test():
    time.sleep(3)  # Wait for server to start
    
    # Register a test user
    signup_payload = {
        "email": f"test_user_{int(time.time())}@example.com",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post("https://laibaasif-chatbot.hf.space/api/auth/signup", json=signup_payload)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data['access_token']
            user_id = auth_data['user_id']
            print(f"User registered. ID: {user_id}, Token: {token[:20]}...")

            # Try the chat endpoint
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
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    # Start server in a thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Run the test
    run_test()
    
    # Keep the main thread alive for a bit to see server output
    time.sleep(10)