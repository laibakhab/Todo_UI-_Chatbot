#!/usr/bin/env python3
"""
Test script to verify the backend fixes for authentication and database issues.
"""

import requests
import json
from datetime import datetime

BASE_URL = "https://laibaasif-chatbot.hf.space"

def test_backend_connectivity():
    """Test if the backend server is running and accessible."""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ Backend server is running and accessible")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Backend server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Cannot connect to backend server: {e}")
        return False

def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Health check endpoint is working")
            print(f"  Response: {response.json()}")
            return True
        else:
            print(f"✗ Health check endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_signup():
    """Test the signup endpoint."""
    try:
        # Use a unique email for testing
        email = f"test_{int(datetime.now().timestamp())}@example.com"
        payload = {
            "email": email,
            "password": "testpassword123"
        }

        response = requests.post(f"{BASE_URL}/api/auth/signup", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✓ Signup endpoint is working")
            print(f"  User ID: {data.get('user_id')}")
            print(f"  Email: {data.get('email')}")

            # Extract the token for further testing
            token = data.get('access_token')
            if token:
                print("  ✓ Token received successfully")
                return True, token, email
            else:
                print("  ✗ No token received")
                return False, None, email
        else:
            print(f"✗ Signup failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False, None, None
    except Exception as e:
        print(f"✗ Signup test failed: {e}")
        return False, None, None

def test_login(email, password="testpassword123"):
    """Test the login endpoint."""
    try:
        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(f"{BASE_URL}/api/auth/signin", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✓ Login endpoint is working")
            print(f"  User ID: {data.get('user_id')}")
            print(f"  Email: {data.get('email')}")

            # Extract the token for further testing
            token = data.get('access_token')
            if token:
                print("  ✓ Token received successfully")
                return True, token
            else:
                print("  ✗ No token received")
                return False, None
        else:
            print(f"✗ Login failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"✗ Login test failed: {e}")
        return False, None

def test_create_task(token):
    """Test creating a task with authentication."""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "title": "Test Task",
            "description": "This is a test task created via API"
        }

        response = requests.post(f"{BASE_URL}/api/tasks/", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✓ Task creation endpoint is working")
            print(f"  Task ID: {data.get('id')}")
            print(f"  Title: {data.get('title')}")
            print(f"  Completed: {data.get('completed')}")
            return True, data.get('id')
        else:
            print(f"✗ Task creation failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False, None
    except Exception as e:
        print(f"✗ Task creation test failed: {e}")
        return False, None

def test_get_tasks(token):
    """Test getting tasks with authentication."""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✓ Get tasks endpoint is working")
            print(f"  Number of tasks: {len(data)}")
            if data:
                print(f"  First task: {data[0].get('title') if data else 'None'}")
            return True
        else:
            print(f"✗ Get tasks failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Get tasks test failed: {e}")
        return False

def main():
    print("Testing Backend Fixes...")
    print("=" * 50)

    # Test basic connectivity
    if not test_backend_connectivity():
        print("\n❌ Backend server is not running. Please start it with:")
        print("   cd backend && uvicorn src.main:app --reload --port 8000")
        return

    # Test health check
    test_health_check()

    # Test signup
    signup_success, token, email = test_signup()
    if not token:
        # Try to log in with a known user instead
        print("  Trying to log in with test user...")
        login_success, token = test_login("user123@example.com", "testpassword123")
        if not token:
            print("\n❌ Could not obtain authentication token.")
            print("   Make sure you have a valid user in the database.")
            return

    # Test protected endpoints
    if token:
        test_create_task(token)
        test_get_tasks(token)

    print("\n" + "=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    main()