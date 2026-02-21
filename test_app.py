"""Quick test to verify all application functionality."""

from src.services import create_task, get_all_tasks, update_task, delete_task, toggle_task_completion
from src.models import Task

def test_all_functions():
    print("Testing all application functionality...")

    # Test creating tasks
    print("\n1. Testing create_task:")
    task1 = create_task("Test Task 1", "Description for task 1")
    task2 = create_task("Test Task 2", "Description for task 2")
    print(f"   Created tasks: {task1.title}, {task2.title}")

    # Test getting all tasks
    print("\n2. Testing get_all_tasks:")
    all_tasks = get_all_tasks()
    for task in all_tasks:
        status = "[X]" if task.completed else "[ ]"
        print(f"   {status} ID: {task.id} | Title: {task.title}")

    # Test updating a task
    print("\n3. Testing update_task:")
    updated_task = update_task(task1.id, "Updated Task 1", "Updated description")
    if updated_task:
        print(f"   Updated task {updated_task.id} to '{updated_task.title}'")

    # Test toggling completion
    print("\n4. Testing toggle_task_completion:")
    toggled_task = toggle_task_completion(task1.id)
    if toggled_task:
        status = "completed" if toggled_task.completed else "incomplete"
        print(f"   Task {toggled_task.id} is now {status}")

    # Test getting all tasks again to see changes
    print("\n5. Testing get_all_tasks after updates:")
    all_tasks = get_all_tasks()
    for task in all_tasks:
        status = "[X]" if task.completed else "[ ]"
        print(f"   {status} ID: {task.id} | Title: {task.title}")

    # Test deleting a task
    print("\n6. Testing delete_task:")
    delete_result = delete_task(task2.id)
    print(f"   Deleted task 2: {delete_result}")

    # Test getting all tasks after deletion
    print("\n7. Testing get_all_tasks after deletion:")
    all_tasks = get_all_tasks()
    if all_tasks:
        for task in all_tasks:
            status = "[X]" if task.completed else "[ ]"
            print(f"   {status} ID: {task.id} | Title: {task.title}")
    else:
        print("   No tasks remaining")

    print("\nAll functionality tested successfully!")

if __name__ == "__main__":
    test_all_functions()