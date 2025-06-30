import React from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart3, 
  Upload, 
  Search, 
  MessageCircle, 
  FileText,
  Trash2,
  Quote,
  Brain,
  Settings
} from 'lucide-react';
import StatsPanel from './StatsPanel';
import PDFUpload from './PDFUpload';
import KnowledgeSearch from './KnowledgeSearch';

const Sidebar = ({ 
  activeTab, 
  setActiveTab, 
  stats, 
  pdfs, 
  onPDFUpload, 
  onClearMemory 
}) => {
  const tabs = [
    { id: 'stats', label: 'Statistics', icon: BarChart3 },
    { id: 'upload', label: 'Upload PDF', icon: Upload },
    { id: 'search', label: 'Knowledge', icon: Search },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="space-y-4">
      {/* Tab Navigation */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-2">
        <div className="flex space-x-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 flex items-center justify-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-100 text-primary-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span className="hidden sm:inline">{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.2 }}
      >
        {activeTab === 'stats' && (
          <StatsPanel stats={stats} pdfs={pdfs} />
        )}
        
        {activeTab === 'upload' && (
          <PDFUpload onUpload={onPDFUpload} />
        )}
        
        {activeTab === 'search' && (
          <KnowledgeSearch />
        )}
        
        {activeTab === 'settings' && (
          <SettingsPanel onClearMemory={onClearMemory} />
        )}
      </motion.div>
    </div>
  );
};

const SettingsPanel = ({ onClearMemory }) => {
  return (
    <div className="space-y-4">
      <div className="sidebar-section">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Settings className="w-5 h-5 mr-2" />
          Settings
        </h3>
        
        <div className="space-y-4">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Conversation</h4>
            <button
              onClick={onClearMemory}
              className="w-full btn-secondary flex items-center justify-center space-x-2"
            >
              <Trash2 className="w-4 h-4" />
              <span>Clear Memory</span>
            </button>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">About</h4>
            <div className="text-sm text-gray-600 space-y-2">
              <p>
                This chatbot simulates conversations with George Soros, 
                the renowned investor and philosopher.
              </p>
              <p>
                Upload PDFs to expand the knowledge base and get more 
                contextual responses.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar; 