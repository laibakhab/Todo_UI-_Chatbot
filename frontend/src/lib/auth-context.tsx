'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

interface User {
  id: number;
  email: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (email: string, password: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check for existing token on initial load
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser && storedUser !== 'undefined') {
      try {
        const parsedUser = JSON.parse(storedUser);
        if (parsedUser && typeof parsedUser === 'object') {
          setToken(storedToken);
          setUser(parsedUser);
        }
      } catch (error) {
        console.warn('Failed to parse stored user data:', error);
      }
    }

    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://laibaasif-chatbot.hf.space';
      const response = await fetch(`${apiUrl}/api/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        // Handle non-JSON responses gracefully
        const contentType = response.headers.get('content-type');
        let errorData;
        if (contentType && contentType.includes('application/json')) {
          errorData = await response.json();
        } else {
          const textResponse = await response.text();
          errorData = { detail: textResponse || `HTTP error ${response.status}` };
        }

        // Explicitly handle 401 Unauthorized
        if (response.status === 401) {
          throw new Error(errorData.detail || "Invalid email or password");
        }

        throw new Error(errorData.detail || 'Login failed');
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Invalid response format received from server');
      }

      const data = await response.json();
      const { access_token } = data;

      // Handle both nested user object (new) and flat structure (legacy)
      let userObj;
      if (data.user) {
        userObj = data.user;
      } else {
        // Fallback construction from flat fields
        userObj = {
          id: data.user_id,
          email: data.email
        };
      }

      // Save token and user_id to localStorage
      localStorage.setItem('token', access_token);
      if (userObj && userObj.id) {
        localStorage.setItem('user_id', userObj.id.toString());
        localStorage.setItem('user', JSON.stringify(userObj));

        setToken(access_token);
        setUser(userObj);
        router.push('/dashboard');
      } else {
        console.error("Invalid user data received:", data);
        throw new Error("Invalid user data received from server");
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://laibaasif-chatbot.hf.space';
      const response = await fetch(`${apiUrl}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        // Handle non-JSON responses gracefully
        const contentType = response.headers.get('content-type');
        let errorData;
        if (contentType && contentType.includes('application/json')) {
          errorData = await response.json();
        } else {
          const textResponse = await response.text();
          errorData = { detail: textResponse || `HTTP error ${response.status}` };
        }
        throw new Error(errorData.detail || 'Registration failed');
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Invalid response format received from server');
      }

      const data = await response.json();
      const { access_token, user } = data;

      // Save token and user_id to localStorage
      localStorage.setItem('token', access_token);
      localStorage.setItem('user_id', user.id.toString()); // Ensure user ID is stored as string
      localStorage.setItem('user', JSON.stringify(user));

      // Automatically log in after registration
      await login(email, password);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    router.push('/signin');
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};