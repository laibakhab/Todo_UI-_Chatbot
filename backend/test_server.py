import subprocess
import time
import requests
import json

def test_server():
    # Start the server
    proc = subprocess.Popen([
        'python', '-m', 'uvicorn', 'src.main:app', '--host', '0.0.0.0', '--port', '8000'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd='.')
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Test the server is running
        response = requests.get('http://localhost:8000/health')
        print(f"Health check: {response.status_code}, {response.json()}")
        
        # Register a test user
        signup_payload = {
            "email": f"test_user_{int(time.time())}@example.com",
            "password": "securepassword123"
        }
        response = requests.post('http://localhost:8000/api/auth/signup', json=signup_payload)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data['access_token']
            user_id = auth_data['user_id']
            print(f"User registered. ID: {user_id}")
            
            # Try the chat endpoint
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            chat_payload = {
                "message": "Add a task to buy groceries"
            }
            
            print(f"Calling chat endpoint with user_id: {user_id}")
            response = requests.post(f'http://localhost:8000/api/{user_id}/chat', json=chat_payload, headers=headers)
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
        else:
            print(f"Failed to register user: {response.status_code}, {response.text}")
            
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        # Terminate the server
        proc.terminate()
        proc.wait()
        
        # Get any error output
        stdout, stderr = proc.communicate()
        if stderr:
            print("Server errors:")
            print(stderr)

if __name__ == "__main__":
    test_server()