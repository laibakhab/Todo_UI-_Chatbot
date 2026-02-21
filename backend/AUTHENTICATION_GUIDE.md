# Authentication Guide for Todo API

This document explains how to authenticate with the Todo API backend.

## Overview

The Todo API uses JWT (JSON Web Tokens) for authentication. All protected endpoints require a valid JWT token to be included in the request headers.

## Authentication Flow

### 1. Register a New User

To register a new user, send a POST request to the `/api/auth/signup` endpoint:

```bash
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password"
  }'
```

Response:
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "email": "your-email@example.com",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Login to Get Access Token

To log in with existing credentials, send a POST request to the `/api/auth/signin` endpoint:

```bash
curl -X POST "http://localhost:8000/api/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password"
  }'
```

Response:
```json
{
  "message": "Login successful",
  "user_id": 1,
  "email": "your-email@example.com",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Use the Access Token for Protected Endpoints

Once you have an access token, include it in the `Authorization` header for all protected endpoints:

```bash
curl -X GET "http://localhost:8000/api/tasks/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json"
```

## Protected Endpoints

The following endpoints require authentication:

- `/api/tasks/` (GET, POST)
- `/api/tasks/{task_id}` (PUT, DELETE)
- `/api/tasks/{task_id}/toggle` (PATCH)
- `/api/{user_id}/chat` (POST)
- `/api/{user_id}/conversations` (GET)
- `/api/{user_id}/conversations/{conversation_id}/messages` (GET)

## Common Issues and Solutions

### Issue: "Access forbidden. Please check your authentication."

**Possible causes:**
1. No token provided in the Authorization header
2. Invalid or expired token
3. Malformed Authorization header

**Solution:**
- Ensure you're sending the token in the Authorization header as `Bearer <token>`
- Verify that you're using the correct token from the login response
- Check that the token hasn't expired (default is 30 minutes)

### Issue: "Could not validate credentials"

**Possible causes:**
1. Token was tampered with
2. Secret key mismatch (server-side issue)
3. Algorithm mismatch

**Solution:**
- Use a fresh token from a new login
- Contact the administrator if the issue persists

## Token Expiration

Access tokens expire after 30 minutes by default. When a token expires, you'll need to log in again to get a new token.

## Security Best Practices

1. Always use HTTPS in production to protect tokens in transit
2. Store tokens securely on the client side
3. Implement automatic token refresh mechanisms
4. Log out users properly to invalidate sessions (though tokens will still be valid until expiration)

## Example with JavaScript/Fetch

```javascript
// Login and store token
async function login(email, password) {
  const response = await fetch('http://localhost:8000/api/auth/signin', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password })
  });
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  return data;
}

// Use token for authenticated requests
async function getTasks() {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/tasks/', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  
  return response.json();
}
```