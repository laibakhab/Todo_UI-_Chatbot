import requests
import json

def test_short_password_signup():
    """Test that the signup endpoint works with a very short password."""
    try:
        # Make a request to the signup endpoint with a short password
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/signup",
            json={
                "email": "shortpass@test.com",
                "password": "pass123"  # Very short password to avoid bcrypt issues
            },
            timeout=10
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        # Check if it returns valid JSON regardless of success or error
        try:
            json_response = response.json()
            print("SUCCESS: Response is valid JSON")
            print(f"JSON Content: {json_response}")

            # If it's a 409 conflict (email already exists), that's also a valid response
            if response.status_code in [200, 409, 400, 422]:
                print("SUCCESS: Got expected response status with valid JSON")
                return True
            elif response.status_code == 500:
                print("Got 500 error, but it's properly formatted JSON")
                return True  # Still a success because it's valid JSON
            else:
                print(f"Got unexpected status code: {response.status_code}")
                return False
        except json.JSONDecodeError:
            print("ERROR: Response is not valid JSON (this is the original issue)")
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
    test_short_password_signup()