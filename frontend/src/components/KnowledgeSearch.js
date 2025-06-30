import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Quote, Brain, Plus, BookOpen } from 'lucide-react';
import axios from 'axios';
import toast from 'react-hot-toast';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const KnowledgeSearch = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [currentQuote, setCurrentQuote] = useState(null);
  const [isLoadingQuote, setIsLoadingQuote] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [addFormData, setAddFormData] = useState({
    type: 'quote',
    content: '',
    conceptName: '',
    definition: '',
    keyPoints: ''
  });

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/search-concepts?query=${encodeURIComponent(searchQuery)}`);
      
      if (response.data.success) {
        setSearchResults(response.data.results);
      } else {
        toast.error('Search failed');
        setSearchResults([]);
      }
    } catch (error) {
      console.error('Search error:', error);
      toast.error('Failed to search concepts');
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const getRandomQuote = async () => {
    setIsLoadingQuote(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/random-quote`);
      
      if (response.data.success) {
        setCurrentQuote(response.data.quote);
      } else {
        toast.error('Failed to get quote');
      }
    } catch (error) {
      console.error('Quote error:', error);
      toast.error('Failed to get random quote');
    } finally {
      setIsLoadingQuote(false);
    }
  };

  const handleAddContent = async (e) => {
    e.preventDefault();
    
    try {
      if (addFormData.type === 'quote') {
        await axios.post(`${API_BASE_URL}/add-quote`, null, {
          params: { quote: addFormData.content }
        });
        toast.success('Quote added successfully!');
      } else {
        await axios.post(`${API_BASE_URL}/add-concept`, null, {
          params: {
            concept_name: addFormData.conceptName,
            definition: addFormData.definition,
            key_points: addFormData.keyPoints
          }
        });
        toast.success('Concept added successfully!');
      }
      
      setShowAddForm(false);
      setAddFormData({
        type: 'quote',
        content: '',
        conceptName: '',
        definition: '',
        keyPoints: ''
      });
    } catch (error) {
      console.error('Add content error:', error);
      toast.error('Failed to add content');
    }
  };

  return (
    <div className="space-y-4">
      {/* Search Section */}
      <div className="sidebar-section">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Search className="w-5 h-5 mr-2" />
          Search Knowledge
        </h3>
        
        <div className="space-y-3">
          <div className="flex space-x-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search concepts..."
              className="input-field flex-1"
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button
              onClick={handleSearch}
              disabled={isSearching || !searchQuery.trim()}
              className="btn-primary disabled:opacity-50"
            >
              {isSearching ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              ) : (
                <Search className="w-4 h-4" />
              )}
            </button>
          </div>

          {/* Search Results */}
          {searchResults.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-3"
            >
              <h4 className="font-medium text-gray-900">Found Concepts:</h4>
              {searchResults.map((result, index) => (
                <motion.div
                  key={result.concept}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-gray-50 rounded-lg p-3 border border-gray-200"
                >
                  <h5 className="font-medium text-gray-900 mb-1">{result.concept}</h5>
                  <p className="text-sm text-gray-700 mb-2">{result.definition}</p>
                  <div className="space-y-1">
                    {result.key_points.map((point, i) => (
                      <div key={i} className="flex items-start space-x-2">
                        <div className="w-1.5 h-1.5 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-xs text-gray-600">{point}</span>
                      </div>
                    ))}
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </div>
      </div>

      {/* Random Quote Section */}
      <div className="sidebar-section">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Quote className="w-5 h-5 mr-2" />
          Random Quote
        </h3>
        
        <button
          onClick={getRandomQuote}
          disabled={isLoadingQuote}
          className="w-full btn-soros mb-3"
        >
          {isLoadingQuote ? (
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
          ) : (
            <>
              <Quote className="w-4 h-4 mr-2" />
              Get Random Quote
            </>
          )}
        </button>

        {currentQuote && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-soros-50 border border-soros-200 rounded-lg p-4"
          >
            <Quote className="w-5 h-5 text-soros-600 mb-2" />
            <blockquote className="text-sm text-gray-700 italic">
              "{currentQuote}"
            </blockquote>
            <p className="text-xs text-soros-600 mt-2 font-medium">— George Soros</p>
          </motion.div>
        )}
      </div>

      {/* Add Content Section */}
      <div className="sidebar-section">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <Plus className="w-5 h-5 mr-2" />
            Add Content
          </h3>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="text-sm text-primary-600 hover:text-primary-700"
          >
            {showAddForm ? 'Cancel' : 'Add New'}
          </button>
        </div>

        {showAddForm && (
          <motion.form
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            onSubmit={handleAddContent}
            className="space-y-3"
          >
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Content Type
              </label>
              <select
                value={addFormData.type}
                onChange={(e) => setAddFormData(prev => ({ ...prev, type: e.target.value }))}
                className="input-field"
              >
                <option value="quote">Quote</option>
                <option value="concept">Concept</option>
              </select>
            </div>

            {addFormData.type === 'quote' ? (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Quote
                </label>
                <textarea
                  value={addFormData.content}
                  onChange={(e) => setAddFormData(prev => ({ ...prev, content: e.target.value }))}
                  placeholder="Enter a Soros quote..."
                  className="input-field"
                  rows={3}
                  required
                />
              </div>
            ) : (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Concept Name
                  </label>
                  <input
                    type="text"
                    value={addFormData.conceptName}
                    onChange={(e) => setAddFormData(prev => ({ ...prev, conceptName: e.target.value }))}
                    placeholder="e.g., sustainable capitalism"
                    className="input-field"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Definition
                  </label>
                  <textarea
                    value={addFormData.definition}
                    onChange={(e) => setAddFormData(prev => ({ ...prev, definition: e.target.value }))}
                    placeholder="Define the concept..."
                    className="input-field"
                    rows={2}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Key Points (comma-separated)
                  </label>
                  <input
                    type="text"
                    value={addFormData.keyPoints}
                    onChange={(e) => setAddFormData(prev => ({ ...prev, keyPoints: e.target.value }))}
                    placeholder="Point 1, Point 2, Point 3"
                    className="input-field"
                    required
                  />
                </div>
              </>
            )}

            <button type="submit" className="w-full btn-primary">
              Add {addFormData.type === 'quote' ? 'Quote' : 'Concept'}
            </button>
          </motion.form>
        )}
      </div>
    </div>
  );
};

export default KnowledgeSearch; 