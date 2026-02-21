'use client';

import { AuthProvider } from '../lib/auth-context';
import ChatbotIcon from '../components/ChatbotIcon'; // PHASE 3 ADDITION
import './globals.css';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <div className="min-h-screen bg-gray-50">
            {children}
            <ChatbotIcon /> {/* PHASE 3 ADDITION - Floating chat icon */}
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}