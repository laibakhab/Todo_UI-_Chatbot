from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import Dict, Any
from pydantic import BaseModel
from ..db import get_db
from ..models.user import User, UserCreate, hash_password, verify_password
from ..utils.token import create_access_token
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Authentication"])


class UserRegisterRequest(BaseModel):
    """Request model for user registration."""
    email: str
    password: str


class UserLoginRequest(BaseModel):
    """Request model for user login."""
    email: str
    password: str


@router.post("/signup")
def register(user_data: UserRegisterRequest, session: Session = Depends(get_db)) -> Dict[str, Any]:
    """Register a new user."""
    try:
        if not user_data.email or not user_data.password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        if len(user_data.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

        existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password with bcrypt
        password_hash = hash_password(user_data.password)
        logger.info(f"Signup: hashed password for {user_data.email}, scheme={password_hash[:4]}")

        user = User(email=user_data.email, password_hash=password_hash)
        session.add(user)
        session.commit()
        session.refresh(user)

        access_token = create_access_token(data={"user_id": user.id, "email": user.email})
        logger.info(f"User registered successfully: {user.email}")

        return {
            "message": "User registered successfully",
            "user": {"id": user.id, "email": user.email},
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred during registration")


@router.post("/signin")
def login(user_data: UserLoginRequest, session: Session = Depends(get_db)) -> Dict[str, Any]:
    """Authenticate a user and return an access token."""
    try:
        if not user_data.email or not user_data.password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        logger.info(f"Attempting login for email: {user_data.email}")

        user = session.exec(select(User).where(User.email == user_data.email)).first()

        if not user:
            logger.warning(f"Login failed: user not found for email {user_data.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Log hash format to aid debugging (never log the actual hash value)
        hash_scheme = "bcrypt" if user.password_hash.startswith(("$2b$", "$2a$", "$2y$")) else "sha256-legacy"
        logger.info(f"Stored hash scheme for {user_data.email}: {hash_scheme}")

        if not verify_password(user_data.password, user.password_hash):
            logger.warning(f"Login failed: password mismatch for {user_data.email} (scheme={hash_scheme})")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = create_access_token(data={"user_id": user.id, "email": user.email})
        logger.info(f"User logged in successfully: {user.email}")

        return {
            "message": "Login successful",
            "user": {"id": user.id, "email": user.email},
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred during login")


@router.post("/signout")
def signout():
    """Sign out the current user."""
    return {"message": "Successfully signed out"}
