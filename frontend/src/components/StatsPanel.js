import React from 'react';
import { motion } from 'framer-motion';
import { 
  BarChart3, 
  FileText, 
  Quote, 
  Brain, 
  MessageCircle,
  Download,
  File
} from 'lucide-react';

const StatsPanel = ({ stats, pdfs }) => {
  const statCards = [
    {
      title: 'Loaded PDFs',
      value: stats.loaded_pdfs,
      icon: FileText,
      color: 'primary',
      description: 'PDF documents processed'
    },
    {
      title: 'Total Quotes',
      value: stats.total_quotes,
      icon: Quote,
      color: 'soros',
      description: 'Soros quotes in database'
    },
    {
      title: 'Total Concepts',
      value: stats.total_concepts,
      icon: Brain,
      color: 'primary',
      description: 'Philosophical concepts'
    },
    {
      title: 'Messages',
      value: stats.conversation_messages,
      icon: MessageCircle,
      color: 'soros',
      description: 'In current conversation'
    }
  ];

  return (
    <div className="space-y-4">
      {/* Statistics Cards */}
      <div className="sidebar-section">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2" />
          System Statistics
        </h3>
        
        <div className="grid grid-cols-2 gap-3">
          {statCards.map((stat, index) => {
            const Icon = stat.icon;
            const colorClasses = {
              primary: 'from-primary-50 to-primary-100 border-primary-200 text-primary-700',
              soros: 'from-soros-50 to-soros-100 border-soros-200 text-soros-700'
            };
            
            return (
              <motion.div
                key={stat.title}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className={`stat-card bg-gradient-to-br ${colorClasses[stat.color]} border p-3 rounded-lg`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-medium opacity-75">{stat.title}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                  </div>
                  <Icon className="w-6 h-6 opacity-75" />
                </div>
                <p className="text-xs mt-1 opacity-75">{stat.description}</p>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* PDF Information */}
      {pdfs.length > 0 && (
        <div className="sidebar-section">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <File className="w-5 h-5 mr-2" />
            Loaded PDFs
          </h3>
          
          <div className="space-y-3">
            {pdfs.map((pdf, index) => (
              <motion.div
                key={pdf.path}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-gray-50 rounded-lg p-3 border border-gray-200"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <h4 className="font-medium text-gray-900 text-sm truncate">
                      {pdf.path.split('/').pop()}
                    </h4>
                    <div className="flex items-center space-x-4 mt-1 text-xs text-gray-600">
                      <span className="flex items-center">
                        <FileText className="w-3 h-3 mr-1" />
                        {pdf.word_count.toLocaleString()} words
                      </span>
                      <span className="flex items-center">
                        <Quote className="w-3 h-3 mr-1" />
                        {pdf.quotes_extracted} quotes
                      </span>
                      <span className="flex items-center">
                        <Brain className="w-3 h-3 mr-1" />
                        {pdf.concepts_found} concepts
                      </span>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="sidebar-section">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        
        <div className="space-y-2">
          <button className="w-full btn-primary flex items-center justify-center space-x-2">
            <Download className="w-4 h-4" />
            <span>Export Conversation</span>
          </button>
          
          <button className="w-full btn-secondary flex items-center justify-center space-x-2">
            <FileText className="w-4 h-4" />
            <span>View All PDFs</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default StatsPanel; 