import requests
import uuid

BASE_URL = "http://127.0.0.1:8000"

def debug_live():
    # 1. Register/Login User
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    password = "password123"
    print(f"DEBUG: Attempting to register user {email}...")
    
    try:
        # Register
        reg_resp = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": password
        })
        print(f"Register status: {reg_resp.status_code}")
        if reg_resp.status_code not in [200, 201]:
            print(f"Register failed: {reg_resp.text}")
            # Try login if user exists? No, random email.
            return

        # Login
        print("DEBUG: Logging in...")
        login_resp = requests.post(f"{BASE_URL}/api/auth/signin", json={ # Updated to json and correct endpoint
            "email": email,
            "password": password
        })
        print(f"Login status: {login_resp.status_code}")
        if login_resp.status_code != 200:
            print(f"Login failed: {login_resp.text}")
            return
            
        try:
            login_data = login_resp.json() # Use login response which has user_id
            user_id = str(login_data.get("user_id", 1))
            token = login_data["access_token"]
            print(f"DEBUG: Using User ID: {user_id}")
        except:
            print("Could not parse user ID or token from login response")
            return

        # 2. Send Chat Message
        headers = {"Authorization": f"Bearer {token}"}
        print(f"DEBUG: Sending chat message to /api/{user_id}/chat...")
        chat_resp = requests.post(f"{BASE_URL}/api/{user_id}/chat", 
            json={"message": "Add a task to buy debug milk"},
            headers=headers
        )
        
        print(f"Chat Response Status: {chat_resp.status_code}")
        print(f"Chat Response Body: {chat_resp.text}")
        
    except Exception as e:
        print(f"CRITICAL EXCEPTION: {e}")

if __name__ == "__main__":
    debug_live()
