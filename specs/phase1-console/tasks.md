# Todo In-Memory Python Console App - Tasks

## Feature: Todo In-Memory Python Console App

Implementation of a command-line todo application with in-memory storage supporting 5 basic operations: Add, View, Update, Delete, and Mark as Complete/Incomplete.

## Dependencies

- User Story 1 (Add Task) must be completed before User Story 3 (Update Task) and User Story 4 (Delete Task)
- User Story 2 (View Tasks) must be completed before User Story 5 (Mark as Complete)
- Foundational tasks must be completed before any user story tasks

## Parallel Execution Examples

- User Story 3 (Update Task) and User Story 4 (Delete Task) can be developed in parallel after User Story 1 is complete
- User Story 2 (View Tasks) and User Story 5 (Mark as Complete) can be developed in parallel

## Implementation Strategy

- MVP: Complete User Story 1 (Add Task) with minimal UI to demonstrate core functionality
- Incremental delivery: Add one user story at a time, maintaining a working application after each addition
- Test-driven development approach for all business logic

## Phase 1: Setup & Core Model

### Goal
Create the basic project structure and core data model for the todo application.

### Independent Test Criteria
- Project structure is created with proper directories
- Task model is defined with required attributes
- Development environment can be set up using provided instructions

### Tasks

- [x] T001 Create project structure: constitution.md, CLAUDE.md, README.md, specs/phase1-console/, src/, tests/
- [x] T002 [P] Create src/models.py file with Task dataclass containing id (int), title (str), description (str), completed (bool)
- [x] T003 [P] Create pyproject.toml with project configuration and dependencies

## Phase 2: Business Logic & Testing

### Goal
Implement the core business logic for todo operations with comprehensive test coverage.

### Independent Test Criteria
- All business logic functions can be executed independently
- All tests pass for each function
- Error handling is properly implemented

### Tasks

- [x] T004 [P] Create tests/test_services.py with test cases for create_task function
- [x] T005 [P] Create tests/test_services.py with test cases for get_all_tasks function
- [x] T006 [P] Create tests/test_services.py with test cases for update_task function
- [x] T007 [P] Create tests/test_services.py with test cases for delete_task function
- [x] T008 [P] Create tests/test_services.py with test cases for toggle_completion function
- [x] T009 [P] Create src/services.py file with global tasks dictionary for storage
- [x] T010 [P] Implement create_task function in src/services.py with auto-incrementing ID
- [x] T011 [P] Implement get_all_tasks function in src/services.py
- [x] T012 [P] Implement update_task function in src/services.py with error handling for non-existent IDs
- [x] T013 [P] Implement delete_task function in src/services.py with error handling for non-existent IDs
- [x] T014 [P] Implement toggle_completion function in src/services.py with error handling for non-existent IDs
- [x] T015 Run all tests to verify business logic implementation

## Phase 3: [US1] Add Task

### Goal
Implement the ability for users to create new tasks with a title and description.

### User Story
As a user, I want to create new tasks with a title and description, so that I can track what I need to do.

### Independent Test Criteria
- User can add a new task with title and description
- System assigns a unique ID to the task automatically
- Task is stored in memory and persists during the session
- Empty title validation prevents task creation and prompts re-entry

### Tasks

- [x] T016 [P] Create src/cli.py with basic menu structure
- [x] T017 [P] [US1] Implement add_task function in src/cli.py to handle user input
- [x] T018 [P] [US1] Implement input validation for empty title in add_task function
- [x] T019 [P] [US1] Implement call to create_task from services in add_task function
- [x] T020 [P] [US1] Add success/error messages for task creation
- [x] T021 [US1] Test the complete add task flow from UI to storage

## Phase 4: [US2] View Tasks

### Goal
Implement the ability for users to see a list of all their tasks with status indicators.

### User Story
As a user, I want to see a list of all my tasks with status indicators, so that I can understand what tasks I have and their completion status.

### Independent Test Criteria
- All tasks are displayed in a readable format
- Each task shows its unique ID, title, and description
- Status indicator clearly shows whether the task is complete or incomplete
- Tasks are presented in a user-friendly format

### Tasks

- [x] T022 [P] [US2] Implement view_tasks function in src/cli.py to display all tasks
- [x] T023 [P] [US2] Implement status indicators ([X] for complete, [ ] for incomplete) in view_tasks
- [x] T024 [P] [US2] Implement call to get_all_tasks from services in view_tasks function
- [x] T025 [P] [US2] Format output in a user-friendly manner
- [x] T026 [US2] Test the complete view tasks flow from UI to data retrieval

## Phase 5: [US3] Update Task

### Goal
Implement the ability for users to modify the details of an existing task.

### User Story
As a user, I want to modify the details of an existing task, so that I can keep my task information accurate and up to date.

### Independent Test Criteria
- User can specify which task to update using its ID
- User can change the title of the task
- User can change the description of the task
- Updated information is reflected in the task list
- Error handling for non-existent IDs

### Tasks

- [x] T027 [P] [US3] Implement update_task function in src/cli.py to handle user input
- [x] T028 [P] [US3] Implement ID input validation in update_task function
- [x] T029 [P] [US3] Implement call to update_task from services in update_task function
- [x] T030 [P] [US3] Add success/error messages for task update
- [x] T031 [US3] Test the complete update task flow with valid and invalid IDs

## Phase 6: [US4] Delete Task

### Goal
Implement the ability for users to remove tasks that they no longer need.

### User Story
As a user, I want to remove tasks that I no longer need, so that my task list remains relevant and manageable.

### Independent Test Criteria
- User can specify which task to delete using its ID
- Task is removed from the memory storage
- Confirmation is provided to the user after deletion
- Deleted task no longer appears in the task list
- Error handling for non-existent IDs

### Tasks

- [x] T032 [P] [US4] Implement delete_task function in src/cli.py to handle user input
- [x] T033 [P] [US4] Implement ID input validation in delete_task function
- [x] T034 [P] [US4] Implement call to delete_task from services in delete_task function
- [x] T035 [P] [US4] Add confirmation and success/error messages for task deletion
- [x] T036 [US4] Test the complete delete task flow with valid and invalid IDs

## Phase 7: [US5] Mark as Complete

### Goal
Implement the ability for users to toggle the completion status of tasks.

### User Story
As a user, I want to toggle the completion status of tasks, so that I can track which tasks I have completed.

### Independent Test Criteria
- User can specify which task to update using its ID
- Task completion status can be toggled between complete and incomplete
- Status change is immediately reflected in the task list
- Visual indicator shows the current status of each task
- Error handling for non-existent IDs

### Tasks

- [x] T037 [P] [US5] Implement mark_toggle function in src/cli.py to handle user input
- [x] T038 [P] [US5] Implement ID input validation in mark_toggle function
- [x] T039 [P] [US5] Implement call to toggle_completion from services in mark_toggle function
- [x] T040 [P] [US5] Add success/error messages for status toggle
- [x] T041 [US5] Test the complete mark toggle flow with valid and invalid IDs

## Phase 8: User Interface & Menu

### Goal
Implement the main menu loop and integrate all user stories into a cohesive command-line interface.

### Independent Test Criteria
- Main menu provides all required options: Add, View, Update, Delete, Mark Toggle, Exit
- Menu handles invalid selections gracefully
- All user stories are accessible through the menu
- Application runs continuously until user chooses to exit

### Tasks

- [x] T042 [P] Implement main menu loop in src/cli.py with numbered options
- [x] T043 [P] Add menu options: 1. Add Task, 2. View Tasks, 3. Update Task, 4. Delete Task, 5. Mark Toggle, 6. Exit
- [x] T044 [P] Implement error handling for invalid menu selections
- [x] T045 [P] Integrate all user story functions into the main menu
- [x] T046 [P] Add graceful exit functionality
- [x] T047 Test the complete menu flow and all integrated features

## Phase 9: Final Integration

### Goal
Create the entry point for the application and update documentation.

### Independent Test Criteria
- Application can be started with python main.py
- Setup instructions are provided in README.md
- All features work together as a complete application

### Tasks

- [x] T048 Create main.py entry point that initializes and runs the CLI
- [x] T049 Update README.md with UV setup instructions: 'uv venv .venv; source .venv/bin/activate; python main.py'
- [x] T050 [P] Test complete application flow from start to finish
- [x] T051 [P] Verify all user stories work in the integrated application
- [x] T052 [P] Update CLAUDE.md with instructions for code generation using Claude Code
- [x] T053 [P] Final testing and bug fixes