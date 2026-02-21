'use client';

import { useState } from 'react';
import { useAuth } from '../../lib/auth-context';
import { useRouter } from 'next/navigation';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const { register } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    try {
      await register(email, password);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--gray-950)] text-[var(--gray-100)] py-12 px-4 sm:px-6 lg:px-8 fade-in">
      {/* Professional Logo */}
      <div className="absolute top-8 left-1/2 transform -translate-x-1/2">
        <h1 className="text-3xl font-bold font-inter text-[var(--gray-100)]">
          Todo Application
        </h1>
      </div>

      <div className="max-w-md w-full space-y-8 slide-in">
        <div>
          <h2 className="mt-6 text-center text-2xl font-bold font-inter text-[var(--gray-100)]">
            Create your Todo Application account
          </h2>
          <p className="mt-2 text-center text-sm text-[var(--gray-400)]">
            Enter your details to get started
          </p>
        </div>

        <div className="glass-effect rounded-xl p-8 border border-[var(--gray-700)] shadow-lg">
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-lg bg-red-900/30 p-4 border border-[var(--red-500)]">
                <div className="text-sm text-red-400">{error}</div>
              </div>
            )}

            <input type="hidden" name="remember" defaultValue="true" />

            <div className="space-y-4">
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Email address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="appearance-none relative block w-full px-4 py-3 border border-[var(--gray-600)] placeholder-[var(--gray-400)] text-[var(--gray-100)] bg-[var(--gray-800)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--indigo-500)] focus:border-[var(--indigo-500)] sm:text-sm transition-all duration-200"
                  placeholder="EMAIL ADDRESS"
                />
              </div>

              <div>
                <label htmlFor="password" className="sr-only">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none relative block w-full px-4 py-3 border border-[var(--gray-600)] placeholder-[var(--gray-400)] text-[var(--gray-100)] bg-[var(--gray-800)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--indigo-500)] focus:border-[var(--indigo-500)] sm:text-sm transition-all duration-200"
                  placeholder="PASSWORD"
                />
              </div>

              <div>
                <label htmlFor="confirm-password" className="sr-only">
                  Confirm Password
                </label>
                <input
                  id="confirm-password"
                  name="confirm-password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className={`appearance-none relative block w-full px-4 py-3 border border-[var(--gray-600)] placeholder-[var(--gray-400)] text-[var(--gray-100)] bg-[var(--gray-800)] rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--indigo-500)] focus:border-[var(--indigo-500)] sm:text-sm transition-all duration-200 ${
                    password === confirmPassword && confirmPassword !== '' ? 'border-[var(--emerald-500)] ring-2 ring-[var(--emerald-500)]/30' : ''
                  }`}
                  placeholder="CONFIRM PASSWORD"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-[var(--indigo-500)] hover:bg-[var(--indigo-600)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--indigo-500)] transition-colors duration-200 hover-lift"
              >
                SIGN UP
              </button>
            </div>
          </form>

          <div className="mt-6 text-center">
            <a
              href="/signin"
              className="font-medium text-[var(--indigo-500)] hover:text-[var(--indigo-400)] transition-colors duration-200"
            >
              ALREADY HAVE AN ACCOUNT? SIGN IN
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}