#!/usr/bin/env python3
"""
Test script to verify the authentication fix
"""
import requests
import json
import time

def test_authentication_fix():
    print("=== Testing Authentication Fix ===\n")
    
    # Start by testing health
    print("1. Testing backend health...")
    try:
        response = requests.get("https://laibaasif-chatbot.hf.space/health")
        if response.status_code == 200:
            print("   [OK] Backend is healthy")
        else:
            print(f"   [ERROR] Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [ERROR] Could not connect to backend: {e}")
        return False
    
    # Test registration
    print("\n2. Testing user registration...")
    user_email = f"auth_test_{int(time.time())}@example.com"
    signup_payload = {
        "email": user_email,
        "password": "securepassword123"
    }
    
    try:
        response = requests.post("https://laibaasif-chatbot.hf.space/api/auth/signup", json=signup_payload)
        if response.status_code == 200:
            auth_data = response.json()
            print(f"   [OK] User registered successfully (ID: {auth_data['user_id']})")
            token = auth_data['access_token']
        else:
            print(f"   [ERROR] Registration failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Registration error: {e}")
        return False
    
    # Test login with correct credentials
    print("\n3. Testing login with correct credentials...")
    signin_payload = {
        "email": user_email,
        "password": "securepassword123"
    }
    
    try:
        response = requests.post("https://laibaasif-chatbot.hf.space/api/auth/signin", json=signin_payload)
        if response.status_code == 200:
            auth_data = response.json()
            print(f"   [OK] Login successful (ID: {auth_data['user_id']})")
        else:
            print(f"   [ERROR] Login failed: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"   [ERROR] Login error: {e}")
        return False
    
    # Test login with incorrect password
    print("\n4. Testing login with incorrect password (should fail)...")
    wrong_signin_payload = {
        "email": user_email,
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post("https://laibaasif-chatbot.hf.space/api/auth/signin", json=wrong_signin_payload)
        if response.status_code == 401:
            print("   [OK] Login correctly failed with wrong password")
        else:
            print(f"   [ERROR] Login should have failed but got: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [ERROR] Wrong password test error: {e}")
        return False
    
    # Test login with non-existent email
    print("\n5. Testing login with non-existent email (should fail)...")
    fake_signin_payload = {
        "email": "nonexistent@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post("https://laibaasif-chatbot.hf.space/api/auth/signin", json=fake_signin_payload)
        if response.status_code == 401:
            print("   [OK] Login correctly failed with non-existent email")
        else:
            print(f"   [ERROR] Login should have failed but got: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [ERROR] Fake email test error: {e}")
        return False
    
    # Test that we can use the token for protected endpoints
    print("\n6. Testing access to protected endpoint with valid token...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get("https://laibaasif-chatbot.hf.space/api/tasks/", headers=headers)
        if response.status_code == 200:
            print("   [OK] Successfully accessed protected endpoint with token")
        else:
            print(f"   [ERROR] Could not access protected endpoint: {response.status_code}")
            return False
    except Exception as e:
        print(f"   [ERROR] Protected endpoint test error: {e}")
        return False
    
    print("\n=== All authentication tests passed! The issue has been fixed! ===")
    print("\nSummary of fixes:")
    print("- Password hashing and verification working correctly")
    print("- Registration creates users properly")
    print("- Login validates credentials properly")
    print("- Invalid credentials are rejected appropriately")
    print("- Valid tokens work for protected endpoints")
    
    return True

if __name__ == "__main__":
    success = test_authentication_fix()
    if not success:
        print("\nSome tests failed. Please check the authentication implementation.")
        exit(1)
    else:
        print("\nAuthentication system is working perfectly!")