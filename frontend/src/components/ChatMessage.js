import React from 'react';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';
import { User, Brain } from 'lucide-react';

const ChatMessage = ({ message }) => {
  const isUser = message.type === 'user';
  const isSoros = message.type === 'soros';

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`chat-message ${isUser ? 'user' : 'soros'}`}
    >
      <div className="flex items-start space-x-3">
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser 
            ? 'bg-primary-100 text-primary-600' 
            : 'bg-soros-100 text-soros-600'
        }`}>
          {isUser ? (
            <User className="w-4 h-4" />
          ) : (
            <Brain className="w-4 h-4" />
          )}
        </div>

        {/* Message Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-1">
            <span className={`font-medium text-sm ${
              isUser ? 'text-primary-700' : 'text-soros-700'
            }`}>
              {isUser ? 'You' : 'George Soros'}
            </span>
            <span className="text-xs text-gray-500">
              {formatTime(message.timestamp)}
            </span>
          </div>
          
          <div className={`prose prose-sm max-w-none ${
            isUser ? 'text-gray-800' : 'text-gray-700'
          }`}>
            <ReactMarkdown
              components={{
                p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                strong: ({ children }) => (
                  <strong className="font-semibold text-gray-900">{children}</strong>
                ),
                em: ({ children }) => (
                  <em className="italic text-gray-800">{children}</em>
                ),
                blockquote: ({ children }) => (
                  <blockquote className="border-l-4 border-soros-300 pl-4 italic text-gray-700 bg-soros-50 py-2 rounded-r">
                    {children}
                  </blockquote>
                ),
                ul: ({ children }) => (
                  <ul className="list-disc list-inside space-y-1 mb-2">{children}</ul>
                ),
                ol: ({ children }) => (
                  <ol className="list-decimal list-inside space-y-1 mb-2">{children}</ol>
                ),
                li: ({ children }) => (
                  <li className="text-gray-700">{children}</li>
                ),
                code: ({ children }) => (
                  <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono text-gray-800">
                    {children}
                  </code>
                ),
                pre: ({ children }) => (
                  <pre className="bg-gray-100 p-3 rounded-lg overflow-x-auto text-sm">
                    {children}
                  </pre>
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default ChatMessage; 