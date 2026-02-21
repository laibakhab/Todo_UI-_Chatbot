# Phase III Specification: Todo AI Chatbot
## 1. Project Overview
- **Objective**: Integrate an AI chatbot into the existing Todo Full-Stack Web Application to enable natural language interaction with task management features
- **Scope** (integrating into existing Phase 2 TODO app): Enhance the existing Next.js/FastAPI/Neon PostgreSQL application with AI-powered chat capabilities while maintaining all existing functionality
- **Key Goals**: Enable natural language processing for task management, implement MCP tools for task operations, provide seamless integration with existing UI, maintain security and user data isolation
- **Non-Goals** (what is NOT included): Complete UI redesign, changing underlying database schema, replacing existing authentication system, adding new core task management features beyond existing functionality

## 2. Requirements
- **Functional Requirements**:
  1. User can interact with the todo application through natural language commands via chat interface
  2. AI chatbot can interpret natural language and execute corresponding task operations (create, read, update, delete, toggle completion)
  3. Chatbot maintains awareness of authenticated user context and respects data isolation
  4. MCP tools enable AI to perform task operations securely
  5. Natural language commands work in both English and Roman Urdu (optional enhancement)
  6. Chat history is preserved within session context
  7. Error handling for ambiguous or invalid commands

- **Non-functional Requirements**:
  - Stateless architecture: Chatbot maintains minimal state between sessions
  - Scalable: Support concurrent users without performance degradation
  - Secure: Respect existing authentication and authorization boundaries
  - Responsive: AI responses within 3 seconds under normal load
  - Reliable: Graceful degradation when AI services are unavailable

## 3. Technology Stack
| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| AI Service | OpenAI GPT or Compatible API | Latest | Natural language processing and response generation |
| MCP Integration | Model Context Protocol | Standard | Tool integration for task operations |
| Frontend | Next.js 16+ | App Router | Chat UI component and real-time communication |
| Backend | FastAPI | Python 3.13+ | Chat API endpoints and authentication |
| Database | Neon PostgreSQL | Serverless | Session and conversation history storage |
| Real-time | WebSocket | Standard | Bidirectional chat communication |
| Authentication | Better Auth | Latest | User context and permissions |

## 4. Architecture
```
[User]
  ↓ (Natural Language Query)
[Next.js Frontend] ←→ [WebSocket Connection] ←→ [FastAPI Backend]
     ↓ (Authenticated Context)                    ↓ (Security Validation)
[Existing UI]                                [AI Service]
                                                 ↓ (MCP Tools)
                                        [Task Management Services]
                                        [Neon PostgreSQL DB]
```

The architecture maintains clear separation between AI service and existing application. The AI service communicates with backend services through MCP tools, ensuring security boundaries are maintained. Authentication context flows from frontend to AI service to ensure proper user data isolation.

## 5. Database Schema
**Conversation Model**:
- id (UUID, Primary Key)
- user_id (Integer, Foreign Key to Users, Required)
- created_at (DateTime, Required)
- updated_at (DateTime, Required)
- title (String, Optional, max 200)

**Message Model**:
- id (UUID, Primary Key)
- conversation_id (UUID, Foreign Key to Conversations, Required)
- role (String, Required: 'user'/'assistant')
- content (Text, Required)
- timestamp (DateTime, Required)
- metadata (JSON, Optional)

## 6. API Endpoints
| Method | Path | Description | Request Body | Response Body |
|--------|------|-------------|--------------|---------------|
| POST | /api/chat/conversations | Create new conversation | {} | {id, title, created_at} |
| GET | /api/chat/conversations | List user's conversations | {} | Array of {id, title, created_at} |
| POST | /api/chat/conversations/{id}/messages | Send message to conversation | {content: string} | {id, content, role, timestamp} |
| GET | /api/chat/conversations/{id}/messages | Get conversation messages | {} | Array of {id, content, role, timestamp} |
| POST | /api/chat/stream | Stream chat response (WebSocket) | {message: string, conversation_id?: string} | Streaming response chunks |

## 7. MCP Tools Specification
**add_task Tool**:
- Purpose: Create a new task for the authenticated user
- Parameters:
  - title (string, required): Task title
  - description (string, optional): Task description
- Returns: {success: boolean, task_id: integer, message: string}
- Example Input: {"title": "Buy groceries", "description": "Milk, bread, eggs"}
- Example Output: {"success": true, "task_id": 123, "message": "Task 'Buy groceries' created successfully"}

**list_tasks Tool**:
- Purpose: Retrieve all tasks for the authenticated user
- Parameters: {}
- Returns: {tasks: Array of {id: integer, title: string, description: string, completed: boolean}}
- Example Input: {}
- Example Output: {"tasks": [{"id": 1, "title": "Buy groceries", "description": "Milk, bread, eggs", "completed": false}]}

**complete_task Tool**:
- Purpose: Mark a specific task as completed
- Parameters:
  - task_id (integer, required): ID of task to complete
- Returns: {success: boolean, message: string}
- Example Input: {"task_id": 123}
- Example Output: {"success": true, "message": "Task 123 marked as completed"}

**delete_task Tool**:
- Purpose: Remove a task from the user's list
- Parameters:
  - task_id (integer, required): ID of task to delete
- Returns: {success: boolean, message: string}
- Example Input: {"task_id": 123}
- Example Output: {"success": true, "message": "Task 123 deleted successfully"}

**update_task Tool**:
- Purpose: Modify an existing task's details
- Parameters:
  - task_id (integer, required): ID of task to update
  - title (string, optional): New title
  - description (string, optional): New description
  - completed (boolean, optional): New completion status
- Returns: {success: boolean, message: string}
- Example Input: {"task_id": 123, "title": "Buy weekly groceries"}
- Example Output: {"success": true, "message": "Task 123 updated successfully"}

## 8. Agent Behavior & Intent Mapping
| User Says (examples) | Agent Should (tool call + logic) |
|---------------------|----------------------------------|
| "Add a task to buy groceries" | Call add_task with title="buy groceries" |
| "Show me my tasks" | Call list_tasks and format response |
| "Complete task 3" | Call complete_task with task_id=3 |
| "Mark 'groceries' as done" | Find task with title containing 'groceries', call complete_task |
| "Delete the meeting task" | Find task with title containing 'meeting', call delete_task |
| "Update task 2 to 'call dentist'" | Call update_task with task_id=2 and new title |
| "What did I need to do today?" | Call list_tasks and summarize incomplete tasks |
| "Set priority for task 1" | Clarify that priorities aren't supported, suggest rewording |

## 9. Conversation Flow (Step-by-Step)
1. User sends natural language message to chat endpoint
2. System validates user authentication and retrieves user context
3. AI service receives message with user context and conversation history
4. AI determines appropriate MCP tool(s) to call based on intent
5. AI executes MCP tool(s) with proper authentication context
6. Tool responses are processed and formatted into natural language
7. AI generates final response considering conversation history
8. Response is streamed back to user interface
9. Both user message and AI response are stored in conversation history

## 10. Success Criteria & Validation
- **MCP Tools**: Each tool returns correct JSON structure within 2 seconds
- **Authentication**: AI tools respect user boundaries and never access other users' data
- **Response Time**: AI responses delivered within 5 seconds for 95% of requests
- **Natural Language Understanding**: 90% accuracy in mapping common commands to correct tools
- **Error Handling**: Ambiguous commands result in clarifying questions rather than errors
- **Integration**: Chat interface seamlessly integrates with existing UI components
- **Security**: All existing security measures remain intact

**Acceptance Tests**:
1. User can add task via chat: "Add task 'buy milk'" → Task appears in task list
2. User can view tasks via chat: "Show my tasks" → Lists all user tasks
3. User can complete task via chat: "Complete task 1" → Task shows as completed
4. User cannot access other users' data through chat
5. Chat maintains conversation context across multiple exchanges
6. Error messages are helpful when commands are ambiguous
7. Existing UI functionality remains unchanged
8. Authentication requirements are met for all chat operations

## 11. Deliverables Checklist
**Files & Folders to be Created/Updated**:
- `/ai-service/` directory with AI service implementation
- `/backend/src/routers/chat.py` - Chat API endpoints
- `/backend/src/tools/` - MCP tools for task operations
- `/frontend/src/app/chat/` - Chat UI components
- `/frontend/src/components/ChatInterface.jsx` - Main chat component
- Updated `docker-compose.yml` to include AI service
- Updated environment variables for AI service configuration

**Deployment Steps**:
1. Deploy AI service alongside existing backend
2. Update frontend to include chat interface
3. Configure WebSocket connections for real-time communication
4. Test integration with existing authentication system
5. Verify MCP tools work correctly with proper authentication

## 12. Assumptions & Constraints
- Existing authentication system (Better Auth) provides user context to AI service
- User IDs are integers as implemented in Phase 2
- Database schema modifications are limited to chat-specific tables
- AI service runs independently but communicates through existing backend APIs
- Natural language processing happens externally via API (OpenAI or compatible)

## 13. Risks & Mitigations
- **Risk**: AI misinterpreting commands leading to incorrect task operations
  - **Mitigation**: Implement confirmation for destructive operations (deletes, updates)
- **Risk**: Increased latency due to AI processing
  - **Mitigation**: Implement caching and async processing where appropriate
- **Risk**: Security breach through AI service bypassing authentication
  - **Mitigation**: Strict MCP tool validation and authentication context checking
- **Risk**: AI service downtime affecting user experience
  - **Mitigation**: Graceful degradation to traditional UI when AI unavailable