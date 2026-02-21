"""Tests for the services module of the Todo In-Memory Python Console App."""

import pytest
from src.services import (
    create_task,
    get_all_tasks,
    update_task,
    delete_task,
    toggle_task_completion,
    get_task_by_id,
    TASKS,
    reset_task_id_counter,
)


class TestCreateTask:
    """Tests for the create_task function."""

    def setup_method(self):
        """Reset the global TASKS dictionary and ID counter before each test."""
        global TASKS
        TASKS.clear()
        reset_task_id_counter()

    def test_create_task_success(self):
        """Test creating a task successfully."""
        task = create_task("Test Title", "Test Description")

        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False
        assert len(TASKS) == 1

    def test_create_task_auto_increment_id(self):
        """Test that IDs are auto-incremented."""
        task1 = create_task("Title 1", "Description 1")
        task2 = create_task("Title 2", "Description 2")

        assert task1.id == 1
        assert task2.id == 2

    def test_create_task_empty_title_error(self):
        """Test that creating a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            create_task("", "Description")

    def test_create_task_none_title_error(self):
        """Test that creating a task with None title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            create_task(None, "Description")

    def test_create_task_whitespace_title_error(self):
        """Test that creating a task with whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            create_task("   ", "Description")


class TestGetAllTasks:
    """Tests for the get_all_tasks function."""

    def setup_method(self):
        """Reset the global TASKS dictionary and ID counter before each test."""
        global TASKS
        TASKS.clear()
        reset_task_id_counter()

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when none exist."""
        tasks = get_all_tasks()

        assert tasks == []
        assert len(tasks) == 0

    def test_get_all_tasks_with_tasks(self):
        """Test getting all tasks when some exist."""
        create_task("Title 1", "Description 1")
        create_task("Title 2", "Description 2")

        tasks = get_all_tasks()

        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[0].title == "Title 1"
        assert tasks[1].title == "Title 2"

    def test_get_all_tasks_sorted_by_id(self):
        """Test that tasks are returned sorted by ID."""
        # Create tasks in reverse order to test sorting
        create_task("Title 3", "Description 3")  # ID 1
        create_task("Title 2", "Description 2")  # ID 2
        create_task("Title 1", "Description 1")  # ID 3

        tasks = get_all_tasks()

        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3


class TestUpdateTask:
    """Tests for the update_task function."""

    def setup_method(self):
        """Reset the global TASKS dictionary and ID counter before each test."""
        global TASKS
        TASKS.clear()
        reset_task_id_counter()

    def test_update_task_success(self):
        """Test updating a task successfully."""
        original_task = create_task("Original Title", "Original Description")

        updated_task = update_task(
            original_task.id,
            "Updated Title",
            "Updated Description"
        )

        assert updated_task is not None
        assert updated_task.id == original_task.id
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.completed == original_task.completed

    def test_update_task_partial_update(self):
        """Test updating only title or description."""
        original_task = create_task("Original Title", "Original Description")

        # Update only the title
        updated_task = update_task(original_task.id, title="New Title")

        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"

        # Update only the description
        updated_task = update_task(original_task.id, description="New Description")

        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_task_not_found(self):
        """Test updating a task that doesn't exist."""
        result = update_task(999, "New Title", "New Description")

        assert result is None

    def test_update_task_empty_title_error(self):
        """Test that updating with empty title raises ValueError."""
        task = create_task("Original Title", "Original Description")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            update_task(task.id, title="")


class TestDeleteTask:
    """Tests for the delete_task function."""

    def setup_method(self):
        """Reset the global TASKS dictionary and ID counter before each test."""
        global TASKS
        TASKS.clear()
        reset_task_id_counter()

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        task = create_task("Title", "Description")

        result = delete_task(task.id)

        assert result is True
        assert len(TASKS) == 0
        assert get_task_by_id(task.id) is None

    def test_delete_task_not_found(self):
        """Test deleting a task that doesn't exist."""
        result = delete_task(999)

        assert result is False

    def test_delete_task_multiple_tasks(self):
        """Test deleting one task doesn't affect others."""
        task1 = create_task("Title 1", "Description 1")
        task2 = create_task("Title 2", "Description 2")
        task3 = create_task("Title 3", "Description 3")

        result = delete_task(task2.id)

        assert result is True
        assert len(TASKS) == 2
        assert get_task_by_id(task1.id) is not None
        assert get_task_by_id(task2.id) is None
        assert get_task_by_id(task3.id) is not None


class TestToggleTaskCompletion:
    """Tests for the toggle_task_completion function."""

    def setup_method(self):
        """Reset the global TASKS dictionary and ID counter before each test."""
        global TASKS
        TASKS.clear()
        reset_task_id_counter()

    def test_toggle_task_completion_success(self):
        """Test toggling task completion status."""
        task = create_task("Title", "Description")
        # Initially should be False
        assert task.completed is False

        # First toggle should make it True
        toggled_task = toggle_task_completion(task.id)
        assert toggled_task.completed is True

        # Second toggle should make it False again
        toggled_task = toggle_task_completion(task.id)
        assert toggled_task.completed is False

    def test_toggle_task_completion_not_found(self):
        """Test toggling completion for a task that doesn't exist."""
        result = toggle_task_completion(999)

        assert result is None


class TestGetTaskById:
    """Tests for the get_task_by_id function."""

    def setup_method(self):
        """Reset the global TASKS dictionary and ID counter before each test."""
        global TASKS
        TASKS.clear()
        reset_task_id_counter()

    def test_get_task_by_id_success(self):
        """Test getting a task by ID successfully."""
        task = create_task("Title", "Description")

        retrieved_task = get_task_by_id(task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.title == task.title
        assert retrieved_task.description == task.description
        assert retrieved_task.completed == task.completed

    def test_get_task_by_id_not_found(self):
        """Test getting a task that doesn't exist."""
        result = get_task_by_id(999)

        assert result is None