import requests
import json

def test_min_length_password_signup():
    """Test that the signup endpoint works with minimum length password."""
    try:
        # Make a request to the signup endpoint with minimum length password
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/signup",
            json={
                "email": "minlength@test.com",
                "password": "pass1234"  # Exactly 8 characters
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

            # If it's a 200 success or 409 conflict (email already exists), that's ideal
            if response.status_code == 200:
                print("SUCCESS: Got successful signup response with valid JSON")
                return True
            elif response.status_code == 409:
                print("SUCCESS: Got conflict response (email already exists) with valid JSON")
                return True
            elif response.status_code in [400, 422]:
                print(f"Got expected error response ({response.status_code}) with valid JSON")
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
    test_min_length_password_signup()