from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from ..models.user import UserPublic, UserPublicFromToken
from ..utils.token import get_current_user
from ..db import get_db


router = APIRouter()


@router.get("/", response_model=List[TaskPublic])
def get_tasks(
    current_user: UserPublicFromToken = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Get all tasks for the current user."""
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/", response_model=TaskPublic)
def create_task(
    task: TaskCreate,
    current_user: UserPublicFromToken = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Create a new task for the current user."""
    db_task = Task(**task.model_dump(), user_id=current_user.id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: UserPublicFromToken = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Update a task for the current user."""
    # Get the task and ensure it belongs to the current user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: UserPublicFromToken = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Delete a task for the current user."""
    # Get the task and ensure it belongs to the current user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/toggle", response_model=TaskPublic)
def toggle_task_completion(
    task_id: int,
    current_user: UserPublicFromToken = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Toggle the completion status of a task for the current user."""
    # Get the task and ensure it belongs to the current user
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status
    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task