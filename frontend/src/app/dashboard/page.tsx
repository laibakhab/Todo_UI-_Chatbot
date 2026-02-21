'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../lib/auth-context';
import { useRouter } from 'next/navigation';
import TaskList from '../../components/TaskList';
import AddTaskForm from '../../components/AddTaskForm';

export default function DashboardPage() {
  const { user, token, logout } = useAuth();
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) {
      router.push('/signin');
    } else {
      setLoading(false);
    }
  }, [token, router]);

  const handleLogout = () => {
    logout();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--gray-950)] text-[var(--gray-100)] fade-in">
      <nav className="bg-[var(--gray-800)] border-b border-[var(--gray-700)] backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold font-inter text-[var(--gray-100)]">
                Todo Application
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-[var(--gray-400)] font-medium">Welcome to Todo Application, {user?.email}!</span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-white bg-[var(--red-500)] rounded-md hover:bg-red-600 transition-colors duration-200"
              >
                LOGOUT
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-8 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-8 glass-effect rounded-xl p-6 border border-[var(--gray-700)] shadow-lg">
            <AddTaskForm />
          </div>
          <div className="glass-effect rounded-xl p-6 border border-[var(--gray-700)] shadow-lg">
            <TaskList />
          </div>
        </div>
      </main>
    </div>
  );
}