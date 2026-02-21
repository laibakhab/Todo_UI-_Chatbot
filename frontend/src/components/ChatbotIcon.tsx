'use client';

import React, { useState, useEffect } from 'react';
import { FaComments, FaTimes } from 'react-icons/fa';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatbotIcon: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    const savedConversationId = localStorage.getItem('chatbot-conversation-id');
    if (savedConversationId) {
      setConversationId(savedConversationId);
    }
  }, []);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (!token || token === 'undefined') {
      // Add error message to UI
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Please login to use the chatbot.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      return;
    }

    // Add user message to UI immediately
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get user ID from localStorage
      let userId = localStorage.getItem('user_id');
      if (!userId) {
        // Fallback to getting user ID from the stored user object
        const storedUser = localStorage.getItem('user');
        if (storedUser && storedUser !== 'undefined') {
          try {
            const userObj = JSON.parse(storedUser);
            if (userObj && typeof userObj.id !== 'undefined') {
              userId = String(userObj.id); // Ensure it's a string
            }
          } catch (parseError) {
            console.error('Error parsing stored user:', parseError);
          }
        }
      }

      // If still no userId, show error
      if (!userId) {
        throw new Error('User ID not found. Please login again.');
      }

      // Call the backend chat API
      const response = await fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          conversation_id: conversationId || undefined,
          message: inputValue
        })
      });

      if (!response.ok) {
        // Handle different error statuses
        if (response.status === 403) {
          // Show authentication error message
          const errorMessage: ChatMessage = {
            id: `error-${Date.now()}`,
            role: 'assistant',
            content: 'Authentication failed, relogin.',
            timestamp: new Date()
          };
          setMessages(prev => [...prev, errorMessage]);
          throw new Error('Access forbidden. Please check your authentication.');
        } else if (response.status === 401) {
          throw new Error('Unauthorized. Please login again.');
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      }

      const data = await response.json();

      // Save conversation ID to localStorage if new
      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id);
        localStorage.setItem('chatbot-conversation-id', data.conversation_id);
      }

      // Add AI response to messages
      const aiMessage: ChatMessage = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Error message is already added to UI for 403 case
      if (!(error instanceof Error) || !error.message.includes('Access forbidden')) {
        // Add error message to UI only if not already added for 403
        const errorMessage: ChatMessage = {
          id: `error-${Date.now()}`,
          role: 'assistant',
          content: error instanceof Error ? error.message : 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date()
        };

        setMessages(prev => [...prev, errorMessage]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Floating Chatbot Icon */}
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-colors z-50"
          aria-label="Open chat"
        >
          <FaComments size={24} />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-full max-w-md h-[600px] flex flex-col bg-white border border-gray-300 rounded-lg shadow-xl z-50">
          {/* Header */}
          <div className="bg-blue-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <h3 className="font-semibold">TODO Chatbot</h3>
            <button
              onClick={toggleChat}
              className="text-white hover:text-gray-200 focus:outline-none"
              aria-label="Close chat"
            >
              <FaTimes />
            </button>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 mt-8">
                Start a conversation with the TODO chatbot!
              </div>
            ) : (
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'
                      }`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${message.role === 'user'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-200 text-gray-800'
                        }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      <p className="text-xs opacity-70 mt-1">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-200 text-gray-800 max-w-xs px-4 py-2 rounded-lg">
                      <p>Thinking...</p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="border-t p-4 bg-white">
            <div className="flex">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message..."
                className="flex-1 border border-gray-300 rounded-l-lg p-2 resize-none h-12"
                disabled={isLoading}
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !inputValue.trim()}
                className={`px-4 rounded-r-lg ${isLoading || !inputValue.trim()
                    ? 'bg-gray-300 text-gray-500'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
              >
                Send
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Ask me to add, list, complete, delete, or update tasks
            </p>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatbotIcon;