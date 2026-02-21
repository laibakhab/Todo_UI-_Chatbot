# Claude Code Instructions for Todo Console App

This document provides instructions for Claude Code when working with the Todo In-Memory Python Console App.

## Project Overview

The Todo In-Memory Python Console App is a command-line application that allows users to manage tasks in memory. It supports the following operations:
- Add tasks with title and description
- View all tasks with status indicators
- Update task details
- Delete tasks by ID
- Mark tasks as complete/incomplete

## Architecture

The application follows a modular structure:
- `src/models.py` - Contains the Task dataclass definition
- `src/services.py` - Implements all business logic for task management
- `src/cli.py` - Handles the command-line interface and user interactions
- `main.py` - Entry point of the application

## Key Implementation Details

1. **Task Model**:
   - Uses a dataclass with id (int), title (str), description (str), and completed (bool) fields
   - ID is auto-incremented when new tasks are created

2. **Services Layer**:
   - Uses a global dictionary (TASKS) for in-memory storage
   - Provides functions: create_task, get_all_tasks, update_task, delete_task, toggle_task_completion
   - Implements proper error handling for invalid IDs and empty titles

3. **CLI Interface**:
   - Menu-driven interface with numbered options
   - Status indicators: [X] for complete, [ ] for incomplete
   - User-friendly error messages for invalid inputs

## Development Guidelines

When modifying or extending this code:
- Follow PEP 8 style guidelines
- Include docstrings for all functions and classes
- Maintain the separation of concerns between models, services, and CLI
- Preserve the in-memory storage approach (no external persistence)
- Keep error handling user-friendly and descriptive
- Maintain the modular file structure

## Common Tasks

### Adding New Features
- Add new functionality to the appropriate module (models, services, or CLI)
- Update the CLI menu and handlers to include new options if needed
- Ensure new functions follow the same error handling patterns

### Modifying Existing Functions
- Update the function in the services layer
- Update any related CLI handlers if the interface changes
- Test the changes through the command-line interface

### Testing
- The application is designed to be tested manually through the CLI
- Verify all error conditions and edge cases work as expected