import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Upload, 
  FileText, 
  Brain, 
  MessageCircle, 
  Settings, 
  Trash2,
  Quote,
  Search,
  Plus,
  Download,
  AlertCircle,
  CheckCircle,
  Loader
} from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import axios from 'axios';
import ChatMessage from './components/ChatMessage';
import Sidebar from './components/Sidebar';
import PDFUpload from './components/PDFUpload';
import KnowledgeSearch from './components/KnowledgeSearch';
import StatsPanel from './components/StatsPanel';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [stats, setStats] = useState({
    loaded_pdfs: 0,
    total_quotes: 0,
    total_concepts: 0,
    conversation_messages: 0
  });
  const [pdfs, setPdfs] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeTab, setActiveTab] = useState('chat');
  const [apiStatus, setApiStatus] = useState('checking');
  
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
    loadStats();
    loadPDFs();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const checkApiHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      setApiStatus(response.data.chatbot_available ? 'healthy' : 'no-api-key');
    } catch (error) {
      setApiStatus('unavailable');
      console.error('API health check failed:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  const loadPDFs = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/pdfs`);
      setPdfs(response.data);
    } catch (error) {
      console.error('Failed to load PDFs:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/chat`, {
        message: inputMessage,
        use_context: true
      });

      if (response.data.success) {
        const sorosMessage = {
          id: Date.now() + 1,
          type: 'soros',
          content: response.data.response,
          timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, sorosMessage]);
        await loadStats(); // Refresh stats after message
      } else {
        toast.error('Failed to get response from Soros');
      }
    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Failed to send message. Please check your connection.');
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  };

  const handleClearMemory = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/clear-memory`);
      setMessages([]);
      await loadStats();
      toast.success('Conversation memory cleared');
    } catch (error) {
      console.error('Failed to clear memory:', error);
      toast.error('Failed to clear memory');
    }
  };

  const handlePDFUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload-pdf`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        toast.success(`${file.name} uploaded successfully!`);
        await loadStats();
        await loadPDFs();
      } else {
        toast.error(`Failed to upload ${file.name}: ${response.data.error}`);
      }
    } catch (error) {
      console.error('PDF upload error:', error);
      toast.error(`Failed to upload ${file.name}`);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  if (apiStatus === 'checking') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="w-8 h-8 animate-spin mx-auto mb-4 text-primary-600" />
          <p className="text-gray-600">Checking API connection...</p>
        </div>
      </div>
    );
  }

  if (apiStatus === 'unavailable') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">API Unavailable</h2>
          <p className="text-gray-600 mb-4">
            The Soros Chatbot API is not running. Please start the backend server first.
          </p>
          <div className="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
            <p className="font-medium mb-2">To start the backend:</p>
            <code className="block bg-white p-2 rounded border">
              python api/main.py
            </code>
          </div>
        </div>
      </div>
    );
  }

  if (apiStatus === 'no-api-key') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertCircle className="w-12 h-12 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">API Key Required</h2>
          <p className="text-gray-600 mb-4">
            Please set your OpenAI API key to use the Soros Chatbot.
          </p>
          <div className="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
            <p className="font-medium mb-2">Set the environment variable:</p>
            <code className="block bg-white p-2 rounded border">
              export OPENAI_API_KEY="your-api-key-here"
            </code>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <motion.div
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                className="flex items-center space-x-3"
              >
                <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-soros-600 rounded-lg flex items-center justify-center">
                  <Brain className="w-5 h-5 text-white" />
                </div>
                <h1 className="text-xl font-bold text-gradient">
                  Soros Chatbot
                </h1>
              </motion.div>
            </div>
            
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <Settings className="w-5 h-5 text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex gap-6">
          {/* Main Chat Area */}
          <div className={`flex-1 ${sidebarOpen ? 'lg:mr-80' : ''}`}>
            <div className="card h-[calc(100vh-12rem)] flex flex-col">
              {/* Chat Messages */}
              <div className="flex-1 overflow-y-auto chat-container p-6">
                <AnimatePresence>
                  {messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                    >
                      <ChatMessage message={message} />
                    </motion.div>
                  ))}
                </AnimatePresence>
                
                {isTyping && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="chat-message soros"
                  >
                    <div className="flex items-center space-x-2">
                      <div className="typing-indicator">
                        <div className="typing-dot"></div>
                        <div className="typing-dot"></div>
                        <div className="typing-dot"></div>
                      </div>
                      <span className="text-sm text-gray-500">George Soros is thinking...</span>
                    </div>
                  </motion.div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="border-t border-gray-200 p-4">
                <form onSubmit={handleSendMessage} className="flex space-x-4">
                  <div className="flex-1">
                    <input
                      ref={inputRef}
                      type="text"
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Ask George Soros anything..."
                      className="input-field"
                      disabled={isLoading}
                    />
                  </div>
                  <button
                    type="submit"
                    disabled={isLoading || !inputMessage.trim()}
                    className="btn-soros disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? (
                      <Loader className="w-5 h-5 animate-spin" />
                    ) : (
                      <Send className="w-5 h-5" />
                    )}
                  </button>
                </form>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <AnimatePresence>
            {sidebarOpen && (
              <motion.div
                initial={{ x: 320, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: 320, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="fixed right-6 top-24 w-80 h-[calc(100vh-8rem)] overflow-y-auto"
              >
                <Sidebar
                  activeTab={activeTab}
                  setActiveTab={setActiveTab}
                  stats={stats}
                  pdfs={pdfs}
                  onPDFUpload={handlePDFUpload}
                  onClearMemory={handleClearMemory}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

export default App; 