from mcp import server, std
from mcp.types import Notification, Request
from ..tools.task_tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool
from typing import Dict, Any, Optional
import json
import asyncio
from pydantic import BaseModel


class AddTaskParams(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class ListTasksParams(BaseModel):
    user_id: str


class CompleteTaskParams(BaseModel):
    user_id: str
    task_id: str


class DeleteTaskParams(BaseModel):
    user_id: str
    task_id: str


class UpdateTaskParams(BaseModel):
    user_id: str
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TodoMCPServer:
    def __init__(self):
        self._server = server.Server("TODO MCP")

    async def register_tools(self):
        # Register add_task tool
        @self._server.tool("add_task", "Add a new task", "Add a new task for a user")
        async def add_task_handler(params: AddTaskParams) -> Dict[str, Any]:
            result = add_task_tool(user_id=params.user_id, title=params.title, description=params.description)
            return result

        # Register list_tasks tool
        @self._server.tool("list_tasks", "List user's tasks", "List all tasks for a user")
        async def list_tasks_handler(params: ListTasksParams) -> Dict[str, Any]:
            result = list_tasks_tool(user_id=params.user_id)
            return result

        # Register complete_task tool
        @self._server.tool("complete_task", "Complete a task", "Mark a task as completed")
        async def complete_task_handler(params: CompleteTaskParams) -> Dict[str, Any]:
            result = complete_task_tool(user_id=params.user_id, task_id=params.task_id)
            return result

        # Register delete_task tool
        @self._server.tool("delete_task", "Delete a task", "Delete a task")
        async def delete_task_handler(params: DeleteTaskParams) -> Dict[str, Any]:
            result = delete_task_tool(user_id=params.user_id, task_id=params.task_id)
            return result

        # Register update_task tool
        @self._server.tool("update_task", "Update a task", "Update task details")
        async def update_task_handler(params: UpdateTaskParams) -> Dict[str, Any]:
            result = update_task_tool(
                user_id=params.user_id,
                task_id=params.task_id,
                title=params.title,
                description=params.description,
                completed=params.completed
            )
            return result

    def get_server(self):
        return self._server


# Global MCP server instance # PHASE 3 ADDITION
todo_mcp_server = TodoMCPServer()


async def initialize_mcp_server():
    await todo_mcp_server.register_tools()


# Get the actual FastAPI router for inclusion in main app
def get_mcp_router():
    return todo_mcp_server.get_server().router