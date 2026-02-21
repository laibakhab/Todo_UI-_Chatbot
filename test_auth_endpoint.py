import requests
import json
import subprocess
import time
import threading

def test_signup_endpoint():
    """Test that the signup endpoint is available and returns proper JSON."""
    try:
        # Make a request to the signup endpoint
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/signup",
            json={
                "email": "test@example.com",
                "password": "testpass"
            },
            timeout=10
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        # Check if it's a 404 error (which indicates the route doesn't exist)
        if response.status_code == 404:
            print("ERROR: Signup endpoint returns 404 - route doesn't exist")
            return False

        # Try to parse the response as JSON
        try:
            json_response = response.json()
            print("SUCCESS: Response is valid JSON")
            print(f"JSON Content: {json_response}")
            return True
        except json.JSONDecodeError:
            print("ERROR: Response is not valid JSON (causing the frontend error)")
            return False

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Make sure the backend is running on port 8000.")
        return False
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out.")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_signup_endpoint()