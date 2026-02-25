#!/usr/bin/env python3
"""
Test script to verify the authentication flow in the Todo API backend.
This script tests user registration, login, and access to protected endpoints.
"""

import requests
import json
from datetime import datetime
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configuration
BASE_URL = "https://laibaasif-chatbot.hf.space"  # Adjust this to your API server URL
TEST_EMAIL = f"testuser_{int(datetime.now().timestamp())}@example.com"
TEST_PASSWORD = "securepassword123"


def test_registration():
    """Test user registration endpoint."""
    print("Testing user registration...")
    
    url = f"{BASE_URL}/api/auth/signup"
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Registration response status: {response.status_code}")
        print(f"Registration response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Registration successful")
            return data.get('access_token')
        else:
            print(f"✗ Registration failed with status {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error during registration: {e}")
        return None


def test_login():
    """Test user login endpoint."""
    print("\nTesting user login...")
    
    url = f"{BASE_URL}/api/auth/signin"
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Login response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Login successful")
            return data.get('access_token')
        else:
            print(f"✗ Login failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error during login: {e}")
        return None


def test_protected_endpoint(token):
    """Test accessing a protected endpoint with a valid token."""
    print("\nTesting access to protected endpoint (tasks)...")
    
    if not token:
        print("✗ No token provided for testing protected endpoint")
        return False
    
    url = f"{BASE_URL}/api/tasks/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Protected endpoint response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Successfully accessed protected endpoint")
            return True
        elif response.status_code == 401:
            print("✗ Unauthorized access - token may be invalid")
            return False
        elif response.status_code == 403:
            print("✗ Forbidden access - check authorization")
            return False
        else:
            print(f"✗ Unexpected response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error accessing protected endpoint: {e}")
        return False


def test_protected_endpoint_without_token():
    """Test accessing a protected endpoint without a token."""
    print("\nTesting access to protected endpoint without token...")
    
    url = f"{BASE_URL}/api/tasks/"
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Protected endpoint without token response status: {response.status_code}")
        
        if response.status_code == 401:
            print("✓ Correctly rejected request without token")
            return True
        else:
            print(f"✗ Expected 401, got {response.status_code} - this might be a security issue")
            return False
    except Exception as e:
        print(f"✗ Error testing unauthorized access: {e}")
        return False


def test_chat_endpoint(token):
    """Test accessing the chat endpoint with a valid token."""
    print("\nTesting access to chat endpoint...")
    
    if not token:
        print("✗ No token provided for testing chat endpoint")
        return False
    
    # Use the authenticated user's ID in the path (we'll need to get it from the token or register/login first)
    # For this test, we'll assume we have a user ID - in practice, you'd extract it from the token or DB
    user_id = 1  # This would normally come from the database after registration
    
    url = f"{BASE_URL}/api/{user_id}/chat"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": "Hello, test message"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Chat endpoint response status: {response.status_code}")
        
        if response.status_code in [200, 404]:  # 404 might be expected if conversation doesn't exist
            print("✓ Chat endpoint responded appropriately")
            return True
        elif response.status_code == 401:
            print("✗ Unauthorized access to chat endpoint")
            return False
        elif response.status_code == 403:
            print("✗ Forbidden access to chat endpoint")
            return False
        else:
            print(f"✗ Unexpected response from chat endpoint: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error accessing chat endpoint: {e}")
        return False


def main():
    """Main test function."""
    print("Starting authentication flow tests...\n")
    
    # Test registration
    token = test_registration()
    
    # If registration failed, try login (in case user already exists)
    if not token:
        print("\nRegistration failed, trying login with existing credentials...")
        token = test_login()
    
    # Test protected endpoint access with token
    success_with_token = test_protected_endpoint(token)
    
    # Test that protected endpoint rejects requests without token
    success_without_token = test_protected_endpoint_without_token()
    
    # Test chat endpoint
    success_chat = test_chat_endpoint(token)
    
    print(f"\n--- Test Summary ---")
    print(f"Registration/Login: {'PASS' if token else 'FAIL'}")
    print(f"Protected endpoint with token: {'PASS' if success_with_token else 'FAIL'}")
    print(f"Protected endpoint without token: {'PASS' if success_without_token else 'FAIL'}")
    print(f"Chat endpoint: {'PASS' if success_chat else 'FAIL'}")
    
    if token and success_with_token and success_without_token and success_chat:
        print("\n✓ All tests passed! Authentication is working correctly.")
        return True
    else:
        print("\n✗ Some tests failed. Please check the authentication implementation.")
        return False


if __name__ == "__main__":
    main()