import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from src.db import get_engine
from src.models import Task, User
from sqlmodel import select, Session

def test_db_connection():
    print("Testing database connection...")
    
    try:
        engine = get_engine()
        print("Engine created successfully")
        
        with Session(engine) as session:
            print("Session created successfully")
            
            # Test if tables exist by querying users
            try:
                users = session.exec(select(User).limit(1)).all()
                print(f"Query successful. Found {len(users)} users (sample).")
            except Exception as e:
                print(f"Query failed: {e}")
                
            # Test if we can create a task (but don't commit)
            try:
                # Just test the model creation
                task = Task(title="Test task", description="Test description", user_id=1)
                print("Task model instantiated successfully")
            except Exception as e:
                print(f"Task instantiation failed: {e}")
        
        print("Database connection test completed successfully!")
        
    except Exception as e:
        print(f"Database connection test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_db_connection()