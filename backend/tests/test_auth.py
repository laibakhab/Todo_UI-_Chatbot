"""
Basic tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    """Test that the health check endpoint works."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test that the root endpoint works."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_signup_endpoint_exists():
    """Test that the signup endpoint exists and returns valid JSON."""
    # Send a sample signup request
    signup_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = client.post("/api/auth/signup", json=signup_data)

    # The endpoint should exist (not return 404)
    # It may return 409 if email already exists, or 422 if validation fails
    # But it should NOT return 404
    assert response.status_code != 404

    # The response should be valid JSON (not HTML)
    try:
        json_response = response.json()
        # Response should be a dict (JSON object)
        assert isinstance(json_response, dict)
    except Exception:
        # If it's not valid JSON, that's an error
        assert False, "Response is not valid JSON"