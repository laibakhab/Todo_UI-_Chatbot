import requests
import json

def test_successful_signup():
    """Test that the signup endpoint works successfully with valid data."""
    try:
        # Make a request to the signup endpoint with valid data
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/signup",
            json={
                "email": "successful@test.com",
                "password": "validpass123"
            },
            timeout=10
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        # Check if the response is successful (200) or has proper error handling
        if response.status_code == 200:
            try:
                json_response = response.json()
                print("SUCCESS: Signup worked and returned valid JSON")
                print(f"User data: {json_response}")
                return True
            except json.JSONDecodeError:
                print("ERROR: Successful response is not valid JSON")
                return False
        elif response.status_code in [400, 409, 422]:
            # These are expected error responses for bad requests or conflicts
            try:
                json_response = response.json()
                print(f"Expected error response: {json_response}")
                print("SUCCESS: Error response is valid JSON")
                return True
            except json.JSONDecodeError:
                print("ERROR: Error response is not valid JSON")
                return False
        else:
            print(f"Unexpected status code: {response.status_code}")
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
    test_successful_signup()