<!--Sync Impact Report:
Version change: 2.0.0 → 3.0.0
Added AI Chatbot functionality section
Updated architecture to include chatbot integration
Modified features to include AI-powered task management
List of modified principles:
  - IV. Persistent Storage & Security (NON-NEGOTIABLE) → IV. Persistent Storage, Security & AI Integration (NON-NEGOTIABLE)
  - V. Multi-User Authentication & Authorization (NON-NEGOTIABLE) → V. Multi-User Authentication & AI-Powered Authorization (NON-NEGOTIABLE)
  - VI. Full-Stack Architecture (NON-NEGOTIABLE) → VI. Full-Stack AI-Enhanced Architecture (NON-NEGOTIABLE)
Added sections: AI Chatbot Rules, Natural Language Processing, MCP Tools Integration
Templates requiring updates: ✅ Updated /specs, /frontend, /backend structure for AI integration
Follow-up TODOs: None
-->
# Todo AI Chatbot Full-Stack Web Application Constitution

## Core Principles

### I. Spec-Driven First
Every feature and implementation must follow the Specify → Plan → Tasks → Implement cycle. No manual code writing is allowed without proper specifications. Specifications must be refined until Claude Code can generate the implementation correctly. This applies to both traditional features and AI-enhanced functionality.

### II. Agentic Workflow
Leverage Claude Code and Spec-Kit Plus for all development tasks. Use subagents where applicable for reusable intelligence. Maintain a clear separation between business logic understanding and technical implementation. Leverage AI agents for natural language processing and intelligent task management.

### III. Full-Stack Modularity (NON-NEGOTIABLE)
Implement as a full-stack application with clear separation between frontend, backend, and shared specifications. The frontend must be a Next.js application, the backend must be a FastAPI service, and all shared specifications must be stored in a centralized location for consistency. Include dedicated AI chatbot service/module that integrates seamlessly with the existing architecture.

### IV. Persistent Storage, Security & AI Integration (NON-NEGOTIABLE)
Use Neon Serverless PostgreSQL for persistent data storage. All data must be encrypted at rest and in transit. Implement proper database connection pooling and secure data access patterns. Integrate AI model state management and conversation history storage while maintaining security standards. No in-memory storage is allowed for production data.

### V. Multi-User Authentication & AI-Powered Authorization (NON-NEGOTIABLE)
Implement user authentication using Better Auth for JWT token generation. All API endpoints must require JWT authentication. User identity must be extracted from tokens and all database queries must be filtered by authenticated user to ensure strict data isolation between users. AI chatbot responses must be contextualized to authenticated user's tasks and preferences.

### VI. Full-Stack AI-Enhanced Architecture (NON-NEGOTIABLE)
Maintain proper separation of concerns between frontend and backend with AI chatbot integration. The frontend must consume both traditional backend APIs and AI chatbot APIs through REST/WebSocket endpoints. Shared specifications must be maintained for API contracts, database schemas, AI response schemas, and UI components to ensure consistency across the stack. AI chatbot must seamlessly integrate with existing task management functionality.

## Constraints

Technology stack must include: Frontend: Next.js 16+ (App Router), Backend: FastAPI (Python 3.13+), ORM: SQLModel, Database: Neon Serverless PostgreSQL, Authentication: Better Auth issuing JWT tokens, Shared secret via `BETTER_AUTH_SECRET`. AI Integration: OpenAI API or compatible LLM platform, WebSocket support for real-time chat, MCP tools for task automation. Spec-Kit Plus + Claude Code only (no manual coding). Docker Compose for local development.

## Core Features

Implement exactly 5 core features in a multi-user authenticated web context with AI enhancement: Add task (authenticated user can add tasks via both UI and natural language commands through AI chatbot), Delete task (authenticated user can delete their own tasks via UI or AI chatbot commands), Update task details (authenticated user can update their own tasks via UI or AI chatbot), View/List tasks (authenticated user can view only their own tasks via UI or AI chatbot queries), Toggle complete/incomplete (authenticated user can update completion status of their own tasks via UI or AI voice/text commands). Additionally, implement AI-powered features: Natural language task creation and modification, Intelligent task categorization and prioritization, Contextual task suggestions, Voice-to-text task input, AI-powered task summaries and insights.

## Security Rules

All API endpoints require JWT authentication. Backend must verify JWT tokens. User identity must be extracted from token. All database queries MUST be filtered by authenticated user. Unauthorized requests return 401. No user may access another user's data. Authentication must be validated on every request that accesses user-specific data. AI chatbot must respect user boundaries and never expose another user's information. All natural language processing must maintain privacy and not store sensitive user information beyond session scope.

## AI Chatbot Rules

The AI chatbot must operate statelessly between conversations while maintaining short-term memory during active sessions. It must understand natural language commands for task management (add, delete, update, view, toggle completion). The chatbot must integrate with MCP tools to execute task operations. Responses must be personalized to the authenticated user's context. Natural language understanding must support both English and Roman Urdu as optional enhancement. Error handling for AI responses must gracefully degrade to traditional UI when AI services are unavailable.

## Natural Language Processing

The system must implement robust natural language processing for task management commands. Supported commands include: "Add task 'buy groceries'", "Complete task 3", "Update task 2 with new description", "Show me my tasks", "Mark task 'exercise' as incomplete", etc. The NLP system must handle ambiguity by asking clarifying questions. Intent recognition must map natural language to specific API calls for task operations.

## MCP Tools Integration

Integrate Model Context Protocol (MCP) tools for AI-powered task management. Tools must include: create_task_tool, update_task_tool, delete_task_tool, get_tasks_tool, toggle_task_completion_tool. Each tool must validate user permissions before execution. Tools must accept natural language input and convert to structured API calls. All MCP tools must operate within the authenticated user's scope only.

## Project Structure

The project must be implemented as a MONOREPO with the following structure:
- /.spec-kit/config.yaml
- /specs (features, api, database, ui, ai-chatbot specs)
- /frontend (Next.js)
- /backend (FastAPI)
- /ai-service (AI chatbot service with WebSocket support)
- docker-compose.yml
- root-level CLAUDE.md and README.md

## Development Workflow

Follow Spec-Driven Development methodology strictly. Create specifications before any implementation work. Use the Spec-Kit Plus framework to generate plans and tasks. Implement through Claude Code's agentic capabilities rather than manual coding. Each feature must have clear acceptance criteria before implementation. All code must pass through security and authentication validation. AI components must be thoroughly tested for accuracy and safety.

## Governance

This constitution governs all development practices for the Todo AI Chatbot Full-Stack Web Application. All code changes must align with these principles. Amendments require documentation of the change and its impact on existing functionality through a Sync Impact Report. All implementations must pass through the Spec-Plan-Tasks-Implement cycle. AI features must undergo additional safety and usability validation. This constitution serves as a binding development contract for the project.

**Version**: 3.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-02-06