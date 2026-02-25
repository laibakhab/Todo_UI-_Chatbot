'use client';

import { useState } from 'react';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

interface TaskItemProps {
  task: Task;
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: number) => void;
}

export default function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [error, setError] = useState<string | null>(null);

  const handleToggleComplete = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://laibaasif-chatbot.hf.space';

      const response = await fetch(`${apiUrl}/api/tasks/${task.id}/toggle`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          // Token is invalid or expired, redirect to login
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/signin';
          throw new Error('Session expired. Please log in again.');
        }
        // Handle different error statuses
        const contentType = response.headers.get('content-type');
        let errorData;
        if (contentType && contentType.includes('application/json')) {
          errorData = await response.json();
        } else {
          const textResponse = await response.text();
          errorData = { detail: textResponse || `HTTP error ${response.status}` };
        }
        throw new Error(errorData.detail || `Failed to update task: ${response.status}`);
      }

      const updatedTask = await response.json();
      onUpdate(updatedTask);
    } catch (err) {
      if (err instanceof TypeError && err.message.includes('fetch')) {
        setError('Network error: Unable to connect to the server. Please check your connection and try again.');
      } else {
        setError(err instanceof Error ? err.message : 'Error updating task');
      }
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://laibaasif-chatbot.hf.space';

      const response = await fetch(`${apiUrl}/api/tasks/${task.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          description: description || null,
        }),
      });

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          // Token is invalid or expired, redirect to login
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/signin';
          throw new Error('Session expired. Please log in again.');
        }
        // Handle different error statuses
        const contentType = response.headers.get('content-type');
        let errorData;
        if (contentType && contentType.includes('application/json')) {
          errorData = await response.json();
        } else {
          const textResponse = await response.text();
          errorData = { detail: textResponse || `HTTP error ${response.status}` };
        }
        throw new Error(errorData.detail || `Failed to update task: ${response.status}`);
      }

      const updatedTask = await response.json();
      onUpdate(updatedTask);
      setIsEditing(false);
    } catch (err) {
      if (err instanceof TypeError && err.message.includes('fetch')) {
        setError('Network error: Unable to connect to the server. Please check your connection and try again.');
      } else {
        setError(err instanceof Error ? err.message : 'Error updating task');
      }
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://laibaasif-chatbot.hf.space';

      const response = await fetch(`${apiUrl}/api/tasks/${task.id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          // Token is invalid or expired, redirect to login
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/signin';
          throw new Error('Session expired. Please log in again.');
        }
        // Handle different error statuses
        const contentType = response.headers.get('content-type');
        let errorData;
        if (contentType && contentType.includes('application/json')) {
          errorData = await response.json();
        } else {
          const textResponse = await response.text();
          errorData = { detail: textResponse || `HTTP error ${response.status}` };
        }
        throw new Error(errorData.detail || `Failed to delete task: ${response.status}`);
      }

      onDelete(task.id);
    } catch (err) {
      if (err instanceof TypeError && err.message.includes('fetch')) {
        setError('Network error: Unable to connect to the server. Please check your connection and try again.');
      } else {
        setError(err instanceof Error ? err.message : 'Error deleting task');
      }
    }
  };

  if (isEditing) {
    return (
      <li className="p-4 border-b border-[var(--gray-700)] hover-lift transition-all duration-200">
        <form onSubmit={handleUpdate} className="space-y-4">
          {error && (
            <div className="text-sm text-red-400">{error}</div>
          )}
          <div>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="block w-full px-4 py-3 rounded-lg border border-[var(--gray-600)] bg-[var(--gray-800)] text-[var(--gray-100)] placeholder-[var(--gray-400)] focus:outline-none focus:ring-2 focus:ring-[var(--indigo-500)] focus:border-[var(--indigo-500)] sm:text-sm transition-all duration-200"
              required
            />
          </div>
          <div>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="block w-full px-4 py-3 rounded-lg border border-[var(--gray-600)] bg-[var(--gray-800)] text-[var(--gray-100)] placeholder-[var(--gray-400)] focus:outline-none focus:ring-2 focus:ring-[var(--indigo-500)] focus:border-[var(--indigo-500)] sm:text-sm transition-all duration-200"
              rows={3}
            />
          </div>
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={() => setIsEditing(false)}
              className="px-4 py-2 text-sm font-medium text-[var(--gray-400)] border border-[var(--gray-600)] rounded-lg hover:bg-[var(--gray-700)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--indigo-500)] transition-colors duration-200"
            >
              CANCEL
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-[var(--indigo-500)] rounded-lg hover:bg-[var(--indigo-600)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--indigo-500)] transition-colors duration-200"
            >
              SAVE
            </button>
          </div>
        </form>
      </li>
    );
  }

  return (
    <li className="p-4 border-b border-[var(--gray-700)] hover-lift transition-all duration-200 group">
      {error && (
        <div className="text-sm text-red-400 mb-2">{error}</div>
      )}
      <div className="flex items-start">
        <div className="flex items-center h-6 mt-1">
          <input
            id={`completed-${task.id}`}
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleComplete}
            className="h-5 w-5 rounded border-[var(--gray-600)] bg-[var(--gray-800)] text-[var(--indigo-500)] focus:ring-[var(--indigo-500)] focus:ring-offset-0 cursor-pointer transition-all duration-200"
          />
        </div>
        <div className="ml-4 min-w-0 flex-1">
          <p className={`text-base font-medium ${task.completed ? 'line-through text-[var(--emerald-500)]' : 'text-[var(--gray-100)]'} transition-all duration-200`}>
            {task.title}
          </p>
          {task.description && (
            <p className={`text-sm mt-1 ${task.completed ? 'line-through text-[var(--emerald-500)]/70' : 'text-[var(--gray-400)]'}`}>
              {task.description}
            </p>
          )}
        </div>
        <div className="ml-4 flex-shrink-0 flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <button
            onClick={() => setIsEditing(true)}
            className="inline-flex items-center px-3 py-1.5 text-xs font-medium text-[var(--amber-500)] border border-[var(--amber-500)] rounded-lg hover:bg-[var(--amber-500)] hover:text-[var(--gray-950)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--amber-500)] transition-colors duration-200"
          >
            EDIT
          </button>
          <button
            onClick={handleDelete}
            className="inline-flex items-center px-3 py-1.5 text-xs font-medium text-[var(--red-500)] border border-[var(--red-500)] rounded-lg hover:bg-[var(--red-500)] hover:text-[var(--gray-950)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--red-500)] transition-colors duration-200"
          >
            DELETE
          </button>
        </div>
      </div>
    </li>
  );
}