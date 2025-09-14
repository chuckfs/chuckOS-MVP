import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { fileAPI } from '../services/api';
import { BarChart3, PieChart, TrendingUp, HardDrive, Folder, Clock, Zap } from 'lucide-react';
import toast from 'react-hot-toast';

const AnalysisPage = () => {
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisData, setAnalysisData] = useState(null);

  const handleAnalyze = async () => {
    setAnalyzing(true);
    try {
      const results = await fileAPI.analyze();
      setAnalysisData(results);
      toast.success('File system analysis complete!');
    } catch (error) {
      toast.error('Analysis failed. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getCategoryColor = (category) => {
    const colors = {
      'images': 'bg-blue-500',
      'documents': 'bg-green-500',
      'audio': 'bg-purple-500',
      'video': 'bg-red-500',
      'code': 'bg-yellow-500',
      'archives': 'bg-gray-500',
      'other': 'bg-gray-400'
    };
    return colors[category] || 'bg-gray-400';
  };

  const getCategoryIcon = (category) => {
    const icons = {
      'images': '📸',
      'documents': '📄',
      'audio': '🎵',
      'video': '🎬',
      'code': '💻',
      'archives': '📦',
      'other': '📁'
    };
    return icons[category] || '📁';
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">
          File System Analysis
        </h1>
        <p className="text-xl text-gray-200 mb-8">
          Get comprehensive insights about your file organization and discover optimization opportunities
        </p>
      </div>

      {/* Analysis Control */}
      <div className="glass-effect p-8 rounded-2xl text-center">
        <div className="mb-6">
          <BarChart3 className="w-16 h-16 text-blue-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">
            AI-Powered File Analysis
          </h2>
          <p className="text-gray-300">
            Let Jaymi AI analyze your file system to discover patterns, suggest optimizations, and provide insights
          </p>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={analyzing}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-4 rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {analyzing ? (
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
              Analyzing Your Files...
            </div>
          ) : (
            <div className="flex items-center">
              <Zap className="w-5 h-5 mr-2" />
              Start Analysis
            </div>
          )}
        </button>

        {analyzing && (
          <div className="mt-4 text-sm text-gray-300">
            <p>🧠 Scanning file system...</p>
            <p>📊 Learning organization patterns...</p>
            <p>💡 Generating insights...</p>
          </div>
        )}
      </div>

      {/* Analysis Results */}
      {analysisData && (
        <>
          {/* Overview Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="glass-effect p-6 rounded-2xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm mb-1">Total Files</p>
                  <p className="text-2xl font-bold text-white">
                    {analysisData.total_files.toLocaleString()}
                  </p>
                </div>
                <Folder className="w-8 h-8 text-blue-400" />
              </div>
            </div>

            <div className="glass-effect p-6 rounded-2xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm mb-1">Total Size</p>
                  <p className="text-2xl font-bold text-white">
                    {formatFileSize(analysisData.total_size)}
                  </p>
                </div>
                <HardDrive className="w-8 h-8 text-purple-400" />
              </div>
            </div>

            <div className="glass-effect p-6 rounded-2xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm mb-1">Categories</p>
                  <p className="text-2xl font-bold text-white">
                    {Object.keys(analysisData.categories).length}
                  </p>
                </div>
                <PieChart className="w-8 h-8 text-green-400" />
              </div>
            </div>

            <div className="glass-effect p-6 rounded-2xl">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-300 text-sm mb-1">Analyzed</p>
                  <p className="text-2xl font-bold text-white">
                    {new Date(analysisData.analyzed_at).toLocaleDateString()}
                  </p>
                </div>
                <Clock className="w-8 h-8 text-yellow-400" />
              </div>
            </div>
          </div>

          {/* File Categories Breakdown */}
          <div className="glass-effect p-8 rounded-2xl">
            <h2 className="text-2xl font-bold text-white mb-6">File Categories</h2>
            
            <div className="space-y-4">
              {Object.entries(analysisData.categories)
                .sort(([,a], [,b]) => b - a)
                .map(([category, count]) => {
                  const sizeInMB = analysisData.category_sizes[category] || 0;
                  const percentage = (count / analysisData.total_files * 100).toFixed(1);
                  
                  return (
                    <div key={category} className="bg-white bg-opacity-5 p-4 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-3">
                          <span className="text-xl">{getCategoryIcon(category)}</span>
                          <span className="text-white font-medium capitalize">{category}</span>
                        </div>
                        <div className="text-right">
                          <p className="text-white font-bold">{count.toLocaleString()} files</p>
                          <p className="text-gray-400 text-sm">{sizeInMB.toFixed(1)} MB</p>
                        </div>
                      </div>
                      
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${getCategoryColor(category)}`}
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                      
                      <p className="text-gray-400 text-sm mt-1">{percentage}% of total files</p>
                    </div>
                  );
                })}
            </div>
          </div>

          {/* Suggestions */}
          {analysisData.suggestions && analysisData.suggestions.length > 0 && (
            <div className="glass-effect p-8 rounded-2xl">
              <div className="flex items-center mb-6">
                <TrendingUp className="w-6 h-6 text-blue-400 mr-3" />
                <h2 className="text-2xl font-bold text-white">AI Suggestions</h2>
              </div>
              
              <div className="space-y-4">
                {analysisData.suggestions.map((suggestion, index) => (
                  <div key={index} className="bg-white bg-opacity-5 p-6 rounded-lg">
                    <div className="flex items-start space-x-3">
                      <div className={`w-3 h-3 rounded-full mt-2 ${
                        suggestion.priority === 'high' ? 'bg-red-400' :
                        suggestion.priority === 'medium' ? 'bg-yellow-400' : 'bg-green-400'
                      }`}></div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold text-white capitalize">
                            {suggestion.type.replace('_', ' ')}
                          </h3>
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            suggestion.priority === 'high' ? 'bg-red-500 text-white' :
                            suggestion.priority === 'medium' ? 'bg-yellow-500 text-black' : 'bg-green-500 text-white'
                          }`}>
                            {suggestion.priority} priority
                          </span>
                        </div>
                        <p className="text-gray-300">{suggestion.message}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Action Items */}
          <div className="glass-effect p-8 rounded-2xl">
            <h2 className="text-2xl font-bold text-white mb-6">Recommended Actions</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white bg-opacity-5 p-6 rounded-lg">
                <h3 className="text-white font-semibold mb-3">🗂️ Auto Organization</h3>
                <p className="text-gray-300 mb-4">
                  Let AI organize your files based on learned patterns and preferences.
                </p>
                <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors">
                  Coming Soon
                </button>
              </div>
              
              <div className="bg-white bg-opacity-5 p-6 rounded-lg">
                <h3 className="text-white font-semibold mb-3">🔍 Smart Search</h3>
                <p className="text-gray-300 mb-4">
                  Use natural language to find files across your analyzed categories.
                </p>
                <a 
                  href="/search"
                  className="bg-purple-500 text-white px-4 py-2 rounded-lg hover:bg-purple-600 transition-colors inline-block"
                >
                  Start Searching
                </a>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Analysis Features */}
      <div className="glass-effect p-8 rounded-2xl">
        <h2 className="text-2xl font-bold text-white mb-6">Analysis Features</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-white font-semibold mb-2">File Distribution</h3>
            <p className="text-gray-300 text-sm">
              Understand how your files are distributed across different categories and locations.
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-white font-semibold mb-2">Usage Patterns</h3>
            <p className="text-gray-300 text-sm">
              Discover patterns in how you organize and access your files.
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-white font-semibold mb-2">Smart Suggestions</h3>
            <p className="text-gray-300 text-sm">
              Get AI-powered recommendations for optimizing your file organization.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;