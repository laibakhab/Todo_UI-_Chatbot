"""Business logic services for the Todo In-Memory Python Console App."""

from typing import List, Optional
from .models import Task

# Global dictionary to store tasks in memory
TASKS: dict[int, Task] = {}
_next_id = 1


def get_next_id() -> int:
    """Get the next available ID for a task.

    Returns:
        The next available ID
    """
    global _next_id
    return _next_id


def increment_next_id() -> None:
    """Increment the next available ID."""
    global _next_id
    _next_id += 1


def reset_task_id_counter() -> None:
    """Reset the task ID counter to 1. Used primarily for testing."""
    global _next_id
    _next_id = 1


def create_task(title: str, description: str) -> Task:
    """Create a new task with auto-incremented ID.

    Args:
        title: The title of the task
        description: The description of the task

    Returns:
        The created Task object

    Raises:
        ValueError: If title is empty or None
    """
    global _next_id

    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")

    task_id = _next_id
    task = Task(id=task_id, title=title.strip(), description=description.strip() if description else "")
    TASKS[task_id] = task
    _next_id += 1
    return task


def get_all_tasks() -> List[Task]:
    """Get all tasks sorted by ID.

    Returns:
        A list of all Task objects sorted by ID
    """
    return sorted(TASKS.values(), key=lambda x: x.id)


def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
    """Update an existing task.

    Args:
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)

    Returns:
        The updated Task object if found, None otherwise

    Raises:
        ValueError: If the new title is empty
    """
    if task_id not in TASKS:
        return None

    task = TASKS[task_id]

    if title is not None:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        task.title = title.strip()

    if description is not None:
        task.description = description.strip() if description else ""

    return task


def delete_task(task_id: int) -> bool:
    """Delete a task by ID.

    Args:
        task_id: The ID of the task to delete

    Returns:
        True if the task was deleted, False if the task was not found
    """
    if task_id not in TASKS:
        return False

    del TASKS[task_id]
    return True


def toggle_task_completion(task_id: int) -> Optional[Task]:
    """Toggle the completion status of a task.

    Args:
        task_id: The ID of the task to toggle

    Returns:
        The updated Task object if found, None otherwise
    """
    if task_id not in TASKS:
        return None

    task = TASKS[task_id]
    task.completed = not task.completed
    return task


def get_task_by_id(task_id: int) -> Optional[Task]:
    """Get a task by its ID.

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        The Task object if found, None otherwise
    """
    return TASKS.get(task_id)