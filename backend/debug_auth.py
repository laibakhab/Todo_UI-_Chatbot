import sys
import os
from sqlmodel import Session, select, create_engine

# Ensure backend directory is in python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.db import get_engine
from src.models.user import User, verify_password, hash_password

def debug_auth():
    print("--- Starting Auth Debug ---")
    from src.config import settings
    print(f"DEBUG: Using Database URL: {settings.database_url}")
    
    try:
        engine = get_engine()
        with Session(engine) as session:
            # 1. List all users
            print("\n1. Listing all users in DB:")
            users = session.exec(select(User)).all()
            if not users:
                print("   NO USERS FOUND IN DATABASE!")
            else:
                for u in users:
                    print(f"   - ID: {u.id}, Email: {u.email}, Hash Format: {u.password_hash[:10]}... (Len: {len(u.password_hash)})")
            
            # 2. Test Verification with a known password
            print("\n2. Testing password verification logic:")
            test_pass = "password123"
            hashed = hash_password(test_pass)
            print(f"   Generated hash for '{test_pass}': {hashed}")
            is_valid = verify_password(test_pass, hashed)
            print(f"   Verification result (Expected True): {is_valid}")
            
            if not is_valid:
                print("CRITICAL: Newly generated hash failed verification!")
            
            # 3. Interactive check (simulate log in)
            if users:
                target_user = users[0]
                print(f"\n3. Attempting to verify first user ({target_user.email})")
                
                # We can't know the real password, but we can check if the hash looks valid
                if ":" not in target_user.password_hash:
                    print(f"CRITICAL: Password hash for {target_user.email} does NOT contain salt separator ':'")
                    print(f"          Value: {target_user.password_hash}")
                    print("          This user cannot log in with the current logic.")
                else:
                    print("          Hash format looks correct (contains salt).")

            # 4. Create a debug user if needed
            debug_email = "debug@example.com"
            debug_pass = "debug123"
            print(f"\n4. Checking/Creating debug user '{debug_email}'")
            debug_user = session.exec(select(User).where(User.email == debug_email)).first()
            if not debug_user:
                print(f"   Creating {debug_email} with password '{debug_pass}'")
                new_user = User(email=debug_email, password_hash=hash_password(debug_pass))
                session.add(new_user)
                session.commit()
                print("   Debug user created.")
            else:
                print(f"   Debug user {debug_email} already exists. Resetting password to '{debug_pass}'")
                debug_user.password_hash = hash_password(debug_pass)
                session.add(debug_user)
                session.commit()
                print("   Password reset.")
                
            # Verify the debug user
            debug_user = session.exec(select(User).where(User.email == debug_email)).first()
            if verify_password(debug_pass, debug_user.password_hash):
                print(f"SUCCESS: verified {debug_email} with password '{debug_pass}'")
            else:
                print(f"FAILURE: Could not verify {debug_email} immediately after set!")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_auth()
