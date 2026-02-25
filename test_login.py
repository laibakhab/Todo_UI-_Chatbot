import requests
import os

# Test the login endpoint
api_url = os.getenv('NEXT_PUBLIC_API_URL', 'https://laibaasif-chatbot.hf.space')

# Try to login with one of the existing users
test_email = "asifalikhan4485@gmail.com"  # Use one of the existing users
test_password = "password123"  # This is likely the default password

login_data = {
    "email": test_email,
    "password": test_password
}

try:
    response = requests.post(f"{api_url}/api/auth/signin", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")

# Let's also try registration to see if that works
register_data = {
    "email": "testuser@example.com",
    "password": "password123"
}

try:
    response = requests.post(f"{api_url}/api/auth/signup", json=register_data)
    print(f"\nRegistration Status Code: {response.status_code}")
    print(f"Registration Response: {response.json()}")
except Exception as e:
    print(f"Registration Error: {e}")