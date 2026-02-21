import sys
import os
import traceback
from contextlib import redirect_stderr
from io import StringIO

# Capture any errors during import
error_capture = StringIO()
try:
    with redirect_stderr(error_capture):
        # Import the main app
        from src.main import app
        from src.db import get_engine
        from sqlmodel import SQLModel
        
        # Initialize database
        engine = get_engine()
        SQLModel.metadata.create_all(engine)
        print("Database initialized successfully")
        
        # Try to import the chat router specifically
        from src.routers import chat
        print("Chat router imported successfully")
        
        # Try to run a simple test
        import asyncio
        import threading
        import time
        import requests
        
        # Start the server in a thread
        def run_server():
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test basic connectivity
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            print(f"Health check: {response.status_code}, {response.json()}")
        except Exception as e:
            print(f"Health check failed: {e}")
        
        print("Server started successfully")
        
except Exception as e:
    print(f"Error during initialization: {e}")
    traceback.print_exc()
    
# Print any captured errors
captured_errors = error_capture.getvalue()
if captured_errors:
    print("Captured errors:")
    print(captured_errors)