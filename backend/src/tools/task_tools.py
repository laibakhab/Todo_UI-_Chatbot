from typing import Dict, Any, Optional
from sqlmodel import Session, select
from ..models import Task, User, Conversation, Message
from ..db import get_engine
import uuid


def add_task_tool(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    MCP tool for adding a new task for a user.

    Args:
        user_id: The ID of the user who owns the task
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dictionary with task_id, status, and title
    """
    user_id_int = int(user_id)

    # Use a synchronous approach for this tool
    engine = get_engine()
    with Session(engine) as session:
        # Verify user exists
        user = session.get(User, user_id_int)
        if not user:
            return {"error": "User not found", "status": "failed"}

        # Create task using the existing service
        task_data = {"title": title, "description": description or "", "user_id": user_id_int}
        task = Task(**task_data)
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }


def list_tasks_tool(user_id: str) -> Dict[str, Any]:
    """
    MCP tool for listing all tasks for a user.

    Args:
        user_id: The ID of the user whose tasks to list

    Returns:
        Dictionary with tasks array
    """
    user_id_int = int(user_id)

    engine = get_engine()
    with Session(engine) as session:
        # Verify user exists
        user = session.get(User, user_id_int)
        if not user:
            return {"error": "User not found", "status": "failed"}

        # Get all tasks for the user
        statement = select(Task).where(Task.user_id == user_id_int)
        results = session.exec(statement).all()

        tasks = []
        for task in results:
            tasks.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            })

        return {"tasks": tasks}


def complete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    MCP tool for marking a task as completed.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to mark as completed

    Returns:
        Dictionary with status message
    """
    user_id_int = int(user_id)
    task_id_int = int(task_id)

    engine = get_engine()
    with Session(engine) as session:
        # Verify user exists
        user = session.get(User, user_id_int)
        if not user:
            return {"error": "User not found", "status": "failed"}

        # Get the task and verify it belongs to the user
        task = session.get(Task, task_id_int)
        if not task:
            return {"error": "Task not found", "status": "failed"}

        if task.user_id != user_id_int:
            return {"error": "Unauthorized access to task", "status": "failed"}

        # Update the task
        task.completed = True
        session.add(task)
        session.commit()

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }


def delete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    MCP tool for deleting a task.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete

    Returns:
        Dictionary with status message
    """
    user_id_int = int(user_id)
    task_id_int = int(task_id)

    engine = get_engine()
    with Session(engine) as session:
        # Verify user exists
        user = session.get(User, user_id_int)
        if not user:
            return {"error": "User not found", "status": "failed"}

        # Get the task and verify it belongs to the user
        task = session.get(Task, task_id_int)
        if not task:
            return {"error": "Task not found", "status": "failed"}

        if task.user_id != user_id_int:
            return {"error": "Unauthorized access to task", "status": "failed"}

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title
        }


def update_task_tool(user_id: str, task_id: str, title: Optional[str] = None,
                     description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    MCP tool for updating task details.

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: Optional new title
        description: Optional new description
        completed: Optional new completion status

    Returns:
        Dictionary with status message
    """
    user_id_int = int(user_id)
    task_id_int = int(task_id)

    engine = get_engine()
    with Session(engine) as session:
        # Verify user exists
        user = session.get(User, user_id_int)
        if not user:
            return {"error": "User not found", "status": "failed"}

        # Get the task and verify it belongs to the user
        task = session.get(Task, task_id_int)
        if not task:
            return {"error": "Task not found", "status": "failed"}

        if task.user_id != user_id_int:
            return {"error": "Unauthorized access to task", "status": "failed"}

        # Update the task fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        session.add(task)
        session.commit()

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }