import subprocess
import threading
import time
import requests
import json

def run_server():
    """Run the server in a subprocess and capture output"""
    import sys
    import os
    os.chdir(r"D:\Todo_UI _Chatbot\backend")
    
    # Start the server
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "src.main:app", 
        "--host", "127.0.0.1", "--port", "8000", "--log-level", "debug"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Print server output in real-time
    while True:
        output = process.stderr.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    return process

def test_chatbot():
    """Test the chatbot functionality after server starts"""
    time.sleep(3)  # Wait for server to start
    
    # Register a user
    register_payload = {
        "email": "test_chat@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/auth/signup", json=register_payload)
        print(f"Registration: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            user_id = result.get("user_id")
            print(f"Registered user ID: {user_id}")
            
            # Test chatbot
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            chat_payload = {
                "message": "Add a task to buy groceries"
            }
            
            response = requests.post(f"http://127.0.0.1:8000/api/{user_id}/chat", json=chat_payload, headers=headers)
            print(f"Chat Response: {response.status_code}")
            print(f"Response Text: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {json.dumps(result, indent=2)}")
            else:
                print(f"Error: {response.text}")
        else:
            print(f"Registration failed: {response.text}")
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    print("Starting server and test...")
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Run test
    test_chatbot()