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

interface AddTaskFormProps {
  onTaskAdded?: (task: Task) => void;
}

export default function AddTaskForm({ onTaskAdded }: AddTaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found. Please log in.');
      }
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://laibaasif-chatbot.hf.space';

      const response = await fetch(`${apiUrl}/api/tasks`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim() || null,
        }),
      });

      if (!response.ok) {
        // Handle different error statuses
        if (response.status === 401 || response.status === 403) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/signin'; // Redirect to login
          throw new Error('Session expired. Please log in again.');
        }

        const contentType = response.headers.get('content-type');
        let errorData;
        if (contentType && contentType.includes('application/json')) {
          errorData = await response.json();
        } else {
          const textResponse = await response.text();
          errorData = { detail: textResponse || `HTTP error ${response.status}` };
        }
        throw new Error(errorData.detail || `Failed to create task: ${response.status}`);
      }

      const newTask = await response.json();
      setTitle('');
      setDescription('');

      if (onTaskAdded) {
        onTaskAdded(newTask);
      }
    } catch (err) {
      if (err instanceof TypeError && err.message.includes('fetch')) {
        setError('Network error: Unable to connect to the server. Please check your connection and try again.');
      } else {
        setError(err instanceof Error ? err.message : 'Error creating task');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="slide-in">
      <div className="md:grid md:grid-cols-3 md:gap-6">
        <div className="md:col-span-1">
          <h3 className="text-xl font-bold font-inter text-[var(--gray-100)]">Add New Task</h3>
          <p className="mt-2 text-sm text-[var(--gray-400)]">Create a new task for your todo list.</p>
        </div>
        <div className="mt-5 md:mt-0 md:col-span-2">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="rounded-md bg-red-900/30 p-4 border border-[var(--red-500)]">
                <div className="text-sm text-red-400">{error}</div>
              </div>
            )}
            <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
              <div className="sm:col-span-6">
                <label htmlFor="title" className="block text-sm font-medium text-[var(--gray-400)]">
                  TITLE *
                </label>
                <div className="mt-1">
                  <input
                    type="text"
                    id="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="py-3 px-4 block w-full max-w-lg rounded-lg border border-[var(--gray-600)] bg-[var(--gray-800)] text-[var(--gray-100)] placeholder-[var(--gray-400)] focus:outline-none focus:ring-2 focus:ring-[var(--indigo-500)] focus:border-[var(--indigo-500)] sm:max-w-xs sm:text-sm transition-all duration-200"
                    placeholder="Task title"
                    disabled={loading}
                  />
                </div>
              </div>

              <div className="sm:col-span-6">
                <label htmlFor="description" className="block text-sm font-medium text-[var(--gray-400)]">
                  DESCRIPTION
                </label>
                <div className="mt-1">
                  <textarea
                    id="description"
                    rows={3}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="py-3 px-4 block w-full max-w-lg rounded-lg border border-[var(--gray-600)] bg-[var(--gray-800)] text-[var(--gray-100)] placeholder-[var(--gray-400)] focus:outline-none focus:ring-2 focus:ring-[var(--indigo-500)] focus:border-[var(--indigo-500)] sm:text-sm transition-all duration-200"
                    placeholder="Task description (optional)"
                    disabled={loading}
                  />
                </div>
              </div>
            </div>
            <div className="mt-6">
              <button
                type="submit"
                disabled={loading}
                className="inline-flex justify-center py-3 px-6 border border-transparent text-sm font-medium rounded-lg text-white bg-[var(--indigo-500)] hover:bg-[var(--indigo-600)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--indigo-500)] disabled:opacity-50 transition-colors duration-200 hover-lift"
              >
                {loading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    CREATING...
                  </span>
                ) : (
                  'ADD TASK'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}