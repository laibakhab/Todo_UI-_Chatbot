import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from src.db import get_engine
from sqlmodel import text

def check_database_schema():
    print("Checking database schema...")
    
    try:
        engine = get_engine()
        
        # Check if conversation table exists and its structure
        with engine.connect() as conn:
            # Query the conversation table structure
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'conversation'
                ORDER BY ordinal_position;
            """))
            
            columns = result.fetchall()
            print("Conversation table columns:")
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
                
            print()
            
            # Also check the message table
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'message'
                ORDER BY ordinal_position;
            """))
            
            columns = result.fetchall()
            print("Message table columns:")
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
                
    except Exception as e:
        print(f"Error checking database schema: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database_schema()