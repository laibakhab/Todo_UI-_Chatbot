import requests
import json

def verify_original_issues_fixed():
    """
    Verify that the original issues mentioned in the request have been fixed:
    1. POST /api/auth/signup 404 - This should now return 200, 400, 409, or 500 but NOT 404
    2. Frontend getting HTML instead of JSON causing "Unexpected token '<'" - This should now return JSON
    """
    print("=== VERIFICATION TEST FOR ORIGINAL ISSUES ===")
    print("Issue 1: POST /api/auth/signup 404 error")
    print("Issue 2: Frontend getting HTML instead of JSON ('Unexpected token \'<\'')")
    print()

    try:
        # Test that the endpoint exists (not 404)
        response = requests.post(
            "http://127.0.0.1:8000/api/auth/signup",
            json={
                "email": "verification@test.com",
                "password": "verifypass123"
            },
            timeout=10
        )

        print(f"Status Code: {response.status_code}")

        # Check if it's a 404 (original issue)
        if response.status_code == 404:
            print("[FAILED] Original issue NOT fixed - Still getting 404 error")
            return False

        print("[PASSED] No 404 error - Endpoint exists")

        # Check if response is JSON (not HTML)
        try:
            json_response = response.json()
            print("[PASSED] Response is valid JSON (not HTML)")
            print(f"JSON Response: {json_response}")

            # Check if it's a proper error response (not HTML)
            if isinstance(json_response, dict) and 'detail' in json_response:
                print("[PASSED] Error response is properly formatted JSON")
            elif response.status_code == 200:
                print("[PASSED] Success response is properly formatted JSON")

            print()
            print("SUCCESS: Both original issues have been resolved!")
            print("   - No more 404 errors (endpoint exists)")
            print("   - No more HTML responses (always returns JSON)")
            print("   - Frontend will no longer get 'Unexpected token '<'' error")
            return True

        except json.JSONDecodeError:
            print("[FAILED] Original issue NOT fixed - Still getting HTML instead of JSON")
            print(f"Response content: {response.text[:200]}...")
            return False

    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to server. Is the backend running on port 8000?")
        return False
    except requests.exceptions.Timeout:
        print("[ERROR] Request timed out.")
        return False
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return False

if __name__ == "__main__":
    verify_original_issues_fixed()