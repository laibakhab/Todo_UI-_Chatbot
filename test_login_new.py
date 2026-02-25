import requests
import os

# Test the login endpoint
api_url = os.getenv('NEXT_PUBLIC_API_URL', 'https://laibaasif-chatbot.hf.space')

# Register a new user first
register_data = {
    "email": "testuser_new@example.com",
    "password": "password123"
}

try:
    response = requests.post(f"{api_url}/api/auth/signup", json=register_data)
    print(f"Registration Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Registration Response: {response.json()}")
    else:
        print(f"Registration Error: {response.json()}")
except Exception as e:
    print(f"Registration Error: {e}")

# Now try to login with the new user
login_data = {
    "email": "testuser_new@example.com",
    "password": "password123"
}

try:
    response = requests.post(f"{api_url}/api/auth/signin", json=login_data)
    print(f"\nLogin Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Login Response: {response.json()}")
    else:
        print(f"Login Error: {response.json()}")
except Exception as e:
    print(f"Login Error: {e}")