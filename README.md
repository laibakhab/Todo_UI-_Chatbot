# Todo Chatbot Application

This is a full-stack Todo application with an AI chatbot that allows users to manage their tasks through natural language conversations.

## Features

- User authentication (register/login)
- Task management (add, list, update, delete, complete)
- AI-powered chatbot interface
- Conversation history
- Full CRUD operations for tasks

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   
4. Update the `.env` file with your configuration (for local development, you can use the SQLite configuration)

5. Create database tables:
   ```bash
   python create_db_tables.py
   ```

6. Start the backend server:
   ```bash
   python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register a new user
- `POST /api/auth/signin` - Login to existing account
- `POST /api/auth/signout` - Logout

### Tasks
- `GET /api/tasks/` - Get all tasks for the current user
- `POST /api/tasks/` - Create a new task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion status

### Chat
- `POST /api/{user_id}/chat` - Chat with the AI assistant
- `GET /api/{user_id}/conversations` - Get user's conversations
- `GET /api/{user_id}/conversations/{conversation_id}/messages` - Get messages in a conversation

## Usage

1. Open your browser and navigate to `http://localhost:3000` (or the port shown by the frontend server)
2. Register a new account or sign in to an existing one
3. Interact with the chatbot to manage your tasks:
   - "Add a task to buy groceries"
   - "Mark task 1 as complete"
   - "List my tasks"
   - "Delete task 2"

## Development

For development, both servers should be running simultaneously:
- Backend: `https://laibaasif-chatbot.hf.space`
- Frontend: `http://localhost:3000`

The frontend is configured to proxy API requests from `/api/*` to the backend server.

## Troubleshooting

- If you encounter database connection issues, make sure the database URL in `.env` is correct
- If authentication fails, ensure you're sending the JWT token in the Authorization header as `Bearer <token>`
- For frontend issues, check that the `NEXT_PUBLIC_API_URL` in the frontend `.env` points to your backend server