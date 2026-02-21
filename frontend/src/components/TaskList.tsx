'use client';

import { useState, useEffect } from 'react';
import TaskItem from './TaskItem';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      const response = await fetch(`${apiUrl}/api/tasks`, {
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
        throw new Error(errorData.detail || `Failed to fetch tasks: ${response.status}`);
      }

      const data = await response.json();
      setTasks(data);
    } catch (err) {
      if (err instanceof TypeError && err.message.includes('fetch')) {
        setError('Network error: Unable to connect to the server. Please check your connection and try again.');
      } else {
        setError(err instanceof Error ? err.message : 'Error fetching tasks');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleTaskUpdate = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDelete = (taskId: number) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[var(--indigo-500)]"></div>
        </div>
        <p className="mt-4 text-lg text-[var(--gray-400)] font-medium">LOADING TASKS...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg bg-red-900/30 p-4 border border-[var(--red-500)]">
        <div className="text-sm text-red-400">ERROR: {error}</div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="mx-auto w-16 h-16 mb-4 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-[var(--gray-400)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <p className="text-lg text-[var(--gray-400)]">NO TASKS YET. ADD YOUR FIRST TASK!</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg">
      <ul className="divide-y divide-[var(--gray-700)]">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onUpdate={handleTaskUpdate}
            onDelete={handleTaskDelete}
          />
        ))}
      </ul>
    </div>
  );
}