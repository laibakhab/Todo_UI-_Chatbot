from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..db import get_db  # Changed from get_session to get_db
from ..models import User
from sqlalchemy.orm import Session
from ..tools.task_tools import (
    add_task_tool,
    list_tasks_tool,
    complete_task_tool,
    delete_task_tool,
    update_task_tool
)


# Define request/response models for MCP tools
class AddTaskRequest(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class ListTasksRequest(BaseModel):
    user_id: str


class CompleteTaskRequest(BaseModel):
    user_id: str
    task_id: str


class DeleteTaskRequest(BaseModel):
    user_id: str
    task_id: str


class UpdateTaskRequest(BaseModel):
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# Create router for MCP tools
router = APIRouter(prefix="/mcp", tags=["mcp"])


@router.post("/add_task")
def mcp_add_task(request: AddTaskRequest, db: Session = Depends(get_db)):  # Changed dependency
    """MCP tool endpoint for adding a task"""
    result = add_task_tool(user_id=request.user_id, title=request.title, description=request.description)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/list_tasks")
def mcp_list_tasks(request: ListTasksRequest, db: Session = Depends(get_db)):  # Changed dependency
    """MCP tool endpoint for listing tasks"""
    result = list_tasks_tool(user_id=request.user_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/complete_task")
def mcp_complete_task(request: CompleteTaskRequest, db: Session = Depends(get_db)):  # Changed dependency
    """MCP tool endpoint for completing a task"""
    result = complete_task_tool(user_id=request.user_id, task_id=request.task_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/delete_task")
def mcp_delete_task(request: DeleteTaskRequest, db: Session = Depends(get_db)):  # Changed dependency
    """MCP tool endpoint for deleting a task"""
    result = delete_task_tool(user_id=request.user_id, task_id=request.task_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/update_task")
def mcp_update_task(request: UpdateTaskRequest, db: Session = Depends(get_db)):  # Changed dependency
    """MCP tool endpoint for updating a task"""
    result = update_task_tool(
        user_id=request.user_id,
        task_id=request.task_id,
        title=request.title,
        description=request.description,
        completed=request.completed
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result