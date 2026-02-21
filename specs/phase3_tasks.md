# Phase III Tasks: Todo AI Chatbot

## Overview
- Total estimated tasks: 28 tasks
- Main phases: 6 phases covering backend setup, MCP tools, AI integration, frontend, testing, and deployment
- General notes: All tasks must be stateless, reuse existing DB connection, user_id required for authentication and data isolation

## Task List

## Phase 1: Backend Setup & Foundation

### T1.1 - Initialize FastAPI updates for chatbot endpoint
*Description:* Add new dependencies and basic chat route skeleton
*Dependencies:* None
*Files to create/update:* backend/requirements.txt, backend/src/main.py
*Tools/Tech used:* FastAPI, uvicorn
*Success Criteria / Validation:* uvicorn runs, /health endpoint returns {"status": "ok"}
*Prompt Suggestion for AI Code Generator:* "In existing FastAPI app, add 'openai-agents-sdk' to requirements.txt and create a POST /api/{user_id}/chat endpoint skeleton that returns a dummy response. Use existing Neon DB connection."

### T1.2 - Update database models for chat
*Description:* Add Conversation and Message models to existing SQLModel setup
*Dependencies:* T1.1
*Files to create/update:* backend/src/models/chat_models.py
*Tools/Tech used:* SQLModel, Neon PostgreSQL
*Success Criteria / Validation:* Database migrations run successfully with new tables
*Prompt Suggestion for AI Code Generator:* "Create Conversation and Message models using SQLModel. Conversation needs id, user_id (foreign key to users), created_at, updated_at, title. Message needs id, conversation_id (foreign key), role (user/assistant), content, timestamp, metadata. Use UUID for primary keys."

### T1.3 - Create chat API router
*Description:* Add FastAPI router for chat endpoints
*Dependencies:* T1.2
*Files to create/update:* backend/src/routers/chat.py
*Tools/Tech used:* FastAPI, existing authentication
*Success Criteria / Validation:* Routes register without errors, accessible via /api/chat/*
*Prompt Suggestion for AI Code Generator:* "Create a FastAPI router for chat endpoints: GET /conversations (list user's), POST /conversations (create new), GET /conversations/{id}/messages (get conversation messages), POST /conversations/{id}/messages (add message). Use existing auth dependency."

## Phase 2: MCP Tools Implementation

### T2.1 - Create MCP tools module skeleton
*Description:* Initialize MCP tools module for task operations
*Dependencies:* Phase 1 complete
*Files to create/update:* backend/src/tools/task_tools.py
*Tools/Tech used:* FastAPI, SQLModel, existing task models
*Success Criteria / Validation:* Module imports without errors, contains function stubs
*Prompt Suggestion for AI Code Generator:* "Create a module with stubs for 5 MCP tools: add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool. Include proper typing for parameters and return values as per spec."

### T2.2 - Implement add_task MCP tool
*Description:* Create tool for adding new tasks via MCP
*Dependencies:* T2.1
*Files to create/update:* backend/src/tools/task_tools.py
*Tools/Tech used:* SQLModel, existing task models and services
*Success Criteria / Validation:* Tool accepts title/description parameters, creates task for user, returns success JSON
*Prompt Suggestion for AI Code Generator:* "Implement add_task_tool function that accepts title (required) and description (optional) parameters. Use existing task creation logic with proper user_id validation. Return success boolean, task_id, and message."

### T2.3 - Implement list_tasks MCP tool
*Description:* Create tool for retrieving user's tasks
*Dependencies:* T2.2
*Files to create/update:* backend/src/tools/task_tools.py
*Tools/Tech used:* SQLModel, existing task models and services
*Success Criteria / Validation:* Tool returns array of user's tasks with id, title, description, completed fields
*Prompt Suggestion for AI Code Generator:* "Implement list_tasks_tool function that returns all tasks for the authenticated user. Return array with id, title, description, completed properties for each task."

### T2.4 - Implement complete_task MCP tool
*Description:* Create tool for marking tasks as completed
*Dependencies:* T2.3
*Files to create/update:* backend/src/tools/task_tools.py
*Tools/Tech used:* SQLModel, existing task models and services
*Success Criteria / Validation:* Tool accepts task_id, marks as completed, returns success JSON
*Prompt Suggestion for AI Code Generator:* "Implement complete_task_tool function that accepts task_id parameter. Updates task completion status for authenticated user's task. Return success boolean and message."

### T2.5 - Implement delete_task MCP tool
*Description:* Create tool for deleting tasks
*Dependencies:* T2.4
*Files to create/update:* backend/src/tools/task_tools.py
*Tools/Tech used:* SQLModel, existing task models and services
*Success Criteria / Validation:* Tool accepts task_id, deletes task for user, returns success JSON
*Prompt Suggestion for AI Code Generator:* "Implement delete_task_tool function that accepts task_id parameter. Deletes task for authenticated user. Return success boolean and message."

### T2.6 - Implement update_task MCP tool
*Description:* Create tool for updating task details
*Dependencies:* T2.5
*Files to create/update:* backend/src/tools/task_tools.py
*Tools/Tech used:* SQLModel, existing task models and services
*Success Criteria / Validation:* Tool accepts task_id and optional fields, updates task, returns success JSON
*Prompt Suggestion for AI Code Generator:* "Implement update_task_tool function that accepts task_id (required) and optional title, description, completed parameters. Updates task fields for authenticated user. Return success boolean and message."

### T2.7 - Add MCP tool validation
*Description:* Ensure all tools validate user permissions correctly
*Dependencies:* T2.6
*Files to create/update:* backend/src/tools/task_tools.py
*Tools/Tech used:* Existing authentication and authorization
*Success Criteria / Validation:* Tools reject operations on other users' tasks
*Prompt Suggestion for AI Code Generator:* "Add user_id validation to all MCP tools. Verify the task being operated on belongs to the authenticated user. Return error if unauthorized."

## Phase 3: OpenAI Agents SDK Integration

### T3.1 - Initialize AI service
*Description:* Create standalone AI service for chat processing
*Dependencies:* Phase 1 complete
*Files to create/update:* ai-service/requirements.txt, ai-service/src/main.py
*Tools/Tech used:* OpenAI Agents SDK, uvicorn
*Success Criteria / Validation:* Service starts and connects to API, health check endpoint works
*Prompt Suggestion for AI Code Generator:* "Create a new directory ai-service with requirements.txt containing openai and necessary dependencies. Create main.py with basic FastAPI app and health endpoint."

### T3.2 - Implement conversation management
*Description:* Add logic for maintaining conversation state and history
*Dependencies:* T3.1
*Files to create/update:* ai-service/src/conversation_manager.py
*Tools/Tech used:* Backend API client, existing DB connection
*Success Criteria / Validation:* Conversations persist across messages, history accessible
*Prompt Suggestion for AI Code Generator:* "Create ConversationManager class that handles storing/retrieving conversation history. Use backend API to save/load messages to/from database. Include methods for create_conversation(), get_messages(conversation_id), and add_message()."

### T3.3 - Integrate MCP tools with AI service
*Description:* Connect AI service to backend MCP tools
*Dependencies:* T3.2, Phase 2 complete
*Files to create/update:* ai-service/src/mcp_client.py
*Tools/Tech used:* HTTP client, existing MCP tools
*Success Criteria / Validation:* AI service can call MCP tools and receive results
*Prompt Suggestion for AI Code Generator:* "Create MCPClient class that can call backend MCP tools via HTTP. Implement methods to call each of the 5 tools (add_task, list_tasks, etc.) and return their responses in the correct format."

### T3.4 - Create AI agent with tools
*Description:* Implement AI agent that uses MCP tools for task operations
*Dependencies:* T3.3
*Files to create/update:* ai-service/src/agent.py
*Tools/Tech used:* OpenAI Agents SDK, MCP tools client
*Success Criteria / Validation:* AI agent responds to queries and calls appropriate tools
*Prompt Suggestion for AI Code Generator:* "Create an AI agent using OpenAI's Assistant API. Register the 5 MCP tools and implement a function that processes user messages, decides which tools to call, and formats responses."

## Phase 4: Chat Endpoint Logic

### T4.1 - Implement stateless chat endpoint
*Description:* Create endpoint that handles chat requests without server-side session state
*Dependencies:* Phase 3 complete
*Files to create/update:* backend/src/routers/chat.py
*Tools/Tech used:* FastAPI, conversation manager, AI agent
*Success Criteria / Validation:* Endpoint accepts user message, returns AI response with tools called
*Prompt Suggestion for AI Code Generator:* "Extend chat router with POST /api/{user_id}/stream endpoint that accepts message and optional conversation_id. Process message through AI agent, save conversation history, return response stream."

### T4.2 - Add chat history management
*Description:* Implement retrieval and storage of conversation history
*Dependencies:* T4.1
*Files to create/update:* backend/src/routers/chat.py, backend/src/services/conversation_service.py
*Tools/Tech used:* SQLModel, existing DB connection
*Success Criteria / Validation:* Chat history persists and can be retrieved for ongoing conversations
*Prompt Suggestion for AI Code Generator:* "Create conversation_service with functions to create, retrieve, and update conversation history. Integrate with chat endpoint to maintain context across messages."

## Phase 5: Frontend ChatKit Integration

### T5.1 - Create chat UI component
*Description:* Build chat interface component with message display and input
*Dependencies:* None
*Files to create/update:* frontend/src/components/ChatInterface.jsx
*Tools/Tech used:* React, Next.js, WebSocket or fetch API
*Success Criteria / Validation:* Component renders, shows message history, accepts user input
*Prompt Suggestion for AI Code Generator:* "Create a React component ChatInterface that displays conversation messages and has an input field for new messages. Include loading states and error handling."

### T5.2 - Implement WebSocket connection for chat
*Description:* Add real-time bidirectional communication for chat
*Dependencies:* T5.1
*Files to create/update:* frontend/src/components/ChatInterface.jsx, frontend/src/lib/chatClient.js
*Tools/Tech used:* WebSocket API, existing auth tokens
*Success Criteria / Validation:* Messages sent and received in real-time
*Prompt Suggestion for AI Code Generator:* "Implement WebSocket connection in chat component. Handle connection open/close, message sending/receiving, and authentication using existing JWT tokens. Update UI when messages arrive."

### T5.3 - Add side icon to existing TODO UI
*Description:* Integrate chat functionality into existing task interface
*Dependencies:* T5.2
*Files to create/update:* frontend/src/components/Layout.jsx, frontend/src/app/chat/page.jsx
*Tools/Tech used:* Next.js, existing UI components
*Success Criteria / Validation:* Chat accessible from main TODO interface via side icon
*Prompt Suggestion for AI Code Generator:* "Add a floating chat icon/button to the main Layout component that opens the chat interface. Create a dedicated page at /chat that renders the ChatInterface component."

## Phase 6: Testing & Deployment

### T6.1 - Create integration tests
*Description:* Test full chat-to-task workflow from frontend to backend
*Dependencies:* All previous phases
*Files to create/update:* backend/tests/test_chat_api.py, backend/tests/test_mcp_tools.py
*Tools/Tech used:* pytest, existing test setup
*Success Criteria / Validation:* Tests verify complete workflow: user message → AI → tool call → DB change
*Prompt Suggestion for AI Code Generator:* "Create integration tests that simulate a full chat session: send 'Add task buy groceries' message, verify AI calls add_task tool, verify task appears in user's task list. Test various commands."

### T6.2 - Update Docker configuration
*Description:* Add AI service to docker-compose.yml
*Dependencies:* Phase 3 complete
*Files to create/update:* docker-compose.yml, ai-service/Dockerfile
*Tools/Tech used:* Docker, Docker Compose
*Success Criteria / Validation:* All services start correctly in containers
*Prompt Suggestion for AI Code Generator:* "Create Dockerfile for ai-service and add it to docker-compose.yml. Configure proper networking between services, environment variables, and startup dependencies."

### T6.3 - Environment configuration
*Description:* Add environment variables for AI service and update documentation
*Dependencies:* T6.2
*Files to create/update:* .env.example, .env, README.md
*Tools/Tech used:* Environment configuration
*Success Criteria / Validation:* Services start with correct configuration
*Prompt Suggestion for AI Code Generator:* "Update .env.example with new variables needed for AI service (OPENAI_API_KEY, etc.). Update README.md with setup instructions for the new chat functionality."