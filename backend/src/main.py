from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, tasks, chat, mcp  # PHASE 3 ADDITION: Added chat and mcp routers

# Import models to ensure they're registered before relationship resolution
from .models import user, task, chat_models  # PHASE 3 ADDITION: Added chat_models
from .db import get_engine
from sqlmodel import SQLModel

app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://localhost:3004"],  # Allow specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chat.router, prefix="/api", tags=["chat"])  # PHASE 3 ADDITION - Changed to /api to allow /{user_id}/chat
app.include_router(mcp.router, prefix="/api/mcp", tags=["mcp"])  # PHASE 3 ADDITION

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


@app.get("/health")
def health_check():
    return {"status": "healthy"}