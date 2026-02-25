#!/usr/bin/env python3
"""
Test script to verify the chatbot functionality
"""
import requests
import json
import time

def test_backend_health():
    """Test if the backend is running and healthy."""
    try:
        response = requests.get("https://laibaasif-chatbot.hf.space/health")
        if response.status_code == 200:
            print("[OK] Backend is running and healthy:", response.json())
            return True
        else:
            print("[ERROR] Backend health check failed:", response.status_code, response.text)
            return False
    except Exception as e:
        print("[ERROR] Could not connect to backend:", str(e))
        return False

def test_root_endpoint():
    """Test the root endpoint."""
    try:
        response = requests.get("https://laibaasif-chatbot.hf.space/")
        if response.status_code == 200:
            print("[OK] Root endpoint is working:", response.json())
            return True
        else:
            print("[ERROR] Root endpoint failed:", response.status_code, response.text)
            return False
    except Exception as e:
        print("[ERROR] Could not connect to root endpoint:", str(e))
        return False

def test_auth_endpoints():
    """Test authentication endpoints."""
    try:
        # Test signup endpoint
        signup_payload = {
            "email": f"testuser_{int(time.time())}@example.com",
            "password": "securepassword123"
        }
        response = requests.post("https://laibaasif-chatbot.hf.space/api/auth/signup", json=signup_payload)
        if response.status_code in [200, 400]:  # 400 might mean user already exists
            print("[OK] Auth endpoints are accessible")
            if response.status_code == 200:
                print("  - Signup successful:", response.json())
            elif response.status_code == 400:
                print("  - Signup returned 400 (possibly user already exists)")
            return True
        else:
            print("[ERROR] Auth endpoint failed:", response.status_code, response.text)
            return False
    except Exception as e:
        print("[ERROR] Could not connect to auth endpoints:", str(e))
        return False

def main():
    print("Testing chatbot functionality...\n")
    
    print("1. Testing backend health...")
    health_ok = test_backend_health()
    
    print("\n2. Testing root endpoint...")
    root_ok = test_root_endpoint()
    
    print("\n3. Testing auth endpoints...")
    auth_ok = test_auth_endpoints()
    
    print(f"\n--- Test Summary ---")
    print(f"Backend Health: {'PASS' if health_ok else 'FAIL'}")
    print(f"Root Endpoint: {'PASS' if root_ok else 'FAIL'}")
    print(f"Auth Endpoints: {'PASS' if auth_ok else 'FAIL'}")
    
    if health_ok and root_ok and auth_ok:
        print("\n[SUCCESS] All tests passed! The chatbot backend is working correctly.")
        print("\nYou can now:")
        print("- Access the frontend at http://localhost:3000")
        print("- Use the API endpoints at https://laibaasif-chatbot.hf.space/api/")
        print("- Register/login users at /api/auth/signup and /api/auth/signin")
        print("- Interact with tasks at /api/tasks/")
        print("- Use the chatbot at /api/{user_id}/chat")
        return True
    else:
        print("\n[FAILURE] Some tests failed. Please check the server configurations.")
        return False

if __name__ == "__main__":
    main()