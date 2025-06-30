import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Upload, FileText, X, CheckCircle, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const PDFUpload = ({ onUpload }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const onDrop = useCallback(async (acceptedFiles) => {
    setUploading(true);
    
    for (const file of acceptedFiles) {
      try {
        await onUpload(file);
        setUploadedFiles(prev => [...prev, { 
          name: file.name, 
          status: 'success',
          timestamp: new Date().toISOString()
        }]);
        toast.success(`${file.name} uploaded successfully!`);
      } catch (error) {
        setUploadedFiles(prev => [...prev, { 
          name: file.name, 
          status: 'error',
          error: error.message,
          timestamp: new Date().toISOString()
        }]);
        toast.error(`Failed to upload ${file.name}`);
      }
    }
    
    setUploading(false);
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: true,
    disabled: uploading
  });

  const removeFile = (index) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-4">
      <div className="sidebar-section">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Upload className="w-5 h-5 mr-2" />
          Upload PDFs
        </h3>
        
        <p className="text-sm text-gray-600 mb-4">
          Upload PDFs containing Soros's writings or related content to expand the knowledge base.
        </p>

        {/* Drop Zone */}
        <div
          {...getRootProps()}
          className={`upload-zone ${isDragActive ? 'active' : ''} ${
            uploading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          <input {...getInputProps()} />
          <div className="space-y-2">
            <Upload className="w-8 h-8 mx-auto text-gray-400" />
            {isDragActive ? (
              <p className="text-primary-600 font-medium">Drop the PDFs here...</p>
            ) : (
              <div>
                <p className="text-gray-600 font-medium">
                  Drag & drop PDFs here, or click to select
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Supports multiple PDF files
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Upload Progress */}
        {uploading && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-blue-50 border border-blue-200 rounded-lg p-3"
          >
            <div className="flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <span className="text-sm text-blue-700">Processing PDFs...</span>
            </div>
          </motion.div>
        )}
      </div>

      {/* Upload History */}
      {uploadedFiles.length > 0 && (
        <div className="sidebar-section">
          <h4 className="font-medium text-gray-900 mb-3">Upload History</h4>
          
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {uploadedFiles.map((file, index) => (
              <motion.div
                key={`${file.name}-${file.timestamp}`}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className={`flex items-center justify-between p-2 rounded-lg border ${
                  file.status === 'success' 
                    ? 'bg-green-50 border-green-200' 
                    : 'bg-red-50 border-red-200'
                }`}
              >
                <div className="flex items-center space-x-2 flex-1 min-w-0">
                  {file.status === 'success' ? (
                    <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0" />
                  )}
                  
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(file.timestamp).toLocaleTimeString()}
                    </p>
                    {file.error && (
                      <p className="text-xs text-red-600 mt-1">{file.error}</p>
                    )}
                  </div>
                </div>
                
                <button
                  onClick={() => removeFile(index)}
                  className="p-1 hover:bg-gray-200 rounded transition-colors"
                >
                  <X className="w-3 h-3 text-gray-500" />
                </button>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Tips */}
      <div className="sidebar-section">
        <h4 className="font-medium text-gray-900 mb-2">Tips</h4>
        <ul className="text-xs text-gray-600 space-y-1">
          <li>• Upload PDFs with Soros's writings for better responses</li>
          <li>• The system will extract quotes and concepts automatically</li>
          <li>• Larger PDFs may take longer to process</li>
          <li>• Supported format: PDF only</li>
        </ul>
      </div>
    </div>
  );
};

export default PDFUpload; 