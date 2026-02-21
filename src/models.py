"""Task dataclass for the Todo In-Memory Python Console App."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a todo task with id, title, description, and completion status."""

    id: int
    title: str
    description: str
    completed: bool = False