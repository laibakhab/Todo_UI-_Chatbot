"""Command-line interface for the Todo In-Memory Python Console App."""

from typing import Optional
import sys
from .services import (
    create_task,
    get_all_tasks,
    update_task,
    delete_task,
    toggle_task_completion,
    get_task_by_id,
)


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "="*40)
    print("TODO APPLICATION")
    print("="*40)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Toggle (Complete/Incomplete)")
    print("6. Exit")
    print("-"*40)


def get_user_choice() -> int:
    """Get and validate user menu choice.

    Returns:
        The user's menu choice as an integer
    """
    while True:
        try:
            choice = int(input("Enter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def add_task() -> None:
    """Handle adding a new task."""
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()

    if not title:
        print("Error: Task title cannot be empty.")
        return

    description = input("Enter task description (optional): ").strip()

    try:
        task = create_task(title, description)
        print(f"Task '{task.title}' added successfully with ID {task.id}")
    except ValueError as e:
        print(f"Error: {e}")


def view_tasks() -> None:
    """Display all tasks with status indicators."""
    print("\n--- All Tasks ---")
    tasks = get_all_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "[X]" if task.completed else "[ ]"
        print(f"{status} ID: {task.id} | Title: {task.title}")
        if task.description:
            print(f"    Description: {task.description}")
        print()


def update_task_ui() -> None:
    """Handle updating an existing task."""
    print("\n--- Update Task ---")

    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Error: Invalid task ID. Please enter a number.")
        return

    task = get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    print(f"Current task: {task.title}")
    if task.description:
        print(f"Current description: {task.description}")

    new_title = input(f"Enter new title (or press Enter to keep '{task.title}'): ").strip()
    new_description = input(f"Enter new description (or press Enter to keep current): ").strip()

    # Use None to indicate no change, otherwise use the new value
    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description else None

    # If user entered empty string for description, we want to clear it
    if new_description == "":
        description_to_update = ""

    try:
        updated_task = update_task(task_id, title_to_update, description_to_update)
        if updated_task:
            print(f"Task ID {task_id} updated successfully.")
        else:
            print(f"Error: Failed to update task ID {task_id}.")
    except ValueError as e:
        print(f"Error: {e}")


def delete_task_ui() -> None:
    """Handle deleting a task."""
    print("\n--- Delete Task ---")

    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Error: Invalid task ID. Please enter a number.")
        return

    task = get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    confirm = input(f"Are you sure you want to delete task '{task.title}'? (y/N): ").lower()
    if confirm in ['y', 'yes']:
        if delete_task(task_id):
            print(f"Task ID {task_id} deleted successfully.")
        else:
            print(f"Error: Failed to delete task ID {task_id}.")
    else:
        print("Deletion cancelled.")


def toggle_task_ui() -> None:
    """Handle toggling task completion status."""
    print("\n--- Toggle Task Completion ---")

    try:
        task_id = int(input("Enter task ID to toggle: "))
    except ValueError:
        print("Error: Invalid task ID. Please enter a number.")
        return

    task = get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} not found.")
        return

    updated_task = toggle_task_completion(task_id)
    if updated_task:
        status = "completed" if updated_task.completed else "incomplete"
        print(f"Task ID {task_id} marked as {status}.")
    else:
        print(f"Error: Failed to toggle task ID {task_id}.")


def run() -> None:
    """Run the main application loop."""
    print("Welcome to the Todo Console Application!")
    print("This application stores tasks in memory only (data will be lost when exiting).")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:
            add_task()
        elif choice == 2:
            view_tasks()
        elif choice == 3:
            update_task_ui()
        elif choice == 4:
            delete_task_ui()
        elif choice == 5:
            toggle_task_ui()
        elif choice == 6:
            print("Thank you for using the Todo Console Application. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")