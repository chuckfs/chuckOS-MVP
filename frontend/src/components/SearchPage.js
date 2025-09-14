import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { fileAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Search, Clock, File, Folder, Star, Filter } from 'lucide-react';
import toast from 'react-hot-toast';

const SearchPage = () => {
  const { user } = useAuth();
  const [query, setQuery] = useState('');
  const [searchHistory, setSearchHistory] = useState([
    'find my photos',
    'documents from last week',
    'large video files',
    'code files in projects'
  ]);

  const [searchResults, setSearchResults] = useState(null);
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async (searchQuery = query) => {
    if (!searchQuery.trim()) {
      toast.error('Please enter a search query');
      return;
    }

    // Check search limits
    if (user.subscription_tier === 'free' && user.searches_this_month >= 100) {
      toast.error('You\'ve reached your monthly search limit. Upgrade to Pro for unlimited searches!');
      return;
    }

    setIsSearching(true);
    try {
      const results = await fileAPI.search(searchQuery);
      setSearchResults(results);
      
      // Add to search history
      if (!searchHistory.includes(searchQuery)) {
        setSearchHistory([searchQuery, ...searchHistory.slice(0, 4)]);
      }
      
      toast.success(`Found ${results.total_found} files in ${results.search_time}s`);
    } catch (error) {
      toast.error('Search failed. Please try again.');
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleQuickSearch = (quickQuery) => {
    setQuery(quickQuery);
    handleSearch(quickQuery);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
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

  const quickSearches = [
    'find my photos',
    'recent documents',
    'large files',
    'music files',
    'code projects',
    'old downloads'
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">
          Smart File Search
        </h1>
        <p className="text-xl text-gray-200 mb-8">
          Find your files using natural language - just describe what you're looking for
        </p>
      </div>

      {/* Search Interface */}
      <div className="glass-effect p-8 rounded-2xl">
        <div className="relative mb-6">
          <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Try: 'find my photos from last week' or 'large video files'"
            className="w-full pl-12 pr-4 py-4 bg-white bg-opacity-10 border border-white border-opacity-20 rounded-lg text-white placeholder-gray-300 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={() => handleSearch()}
            disabled={isSearching}
            className="absolute right-2 top-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-2 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-colors disabled:opacity-50"
          >
            {isSearching ? 'Searching...' : 'Search'}
          </button>
        </div>

        {/* Search Stats */}
        {user && (
          <div className="flex items-center justify-between text-sm text-gray-300 mb-4">
            <span>
              Searches this month: {user.searches_this_month}/
              {user.subscription_tier === 'free' ? '100' : '∞'}
            </span>
            <span className="text-blue-300">
              {user.subscription_tier === 'free' && user.searches_this_month >= 80 ? 
                'Upgrade to Pro for unlimited searches!' : 
                'Powered by Jaymi AI'
              }
            </span>
          </div>
        )}

        {/* Quick Searches */}
        <div>
          <h3 className="text-white font-medium mb-3">Quick Searches</h3>
          <div className="flex flex-wrap gap-2">
            {quickSearches.map((quickQuery, index) => (
              <button
                key={index}
                onClick={() => handleQuickSearch(quickQuery)}
                className="bg-white bg-opacity-10 text-gray-200 px-3 py-1 rounded-full text-sm hover:bg-opacity-20 transition-colors"
              >
                {quickQuery}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Search History */}
      {searchHistory.length > 0 && (
        <div className="glass-effect p-6 rounded-2xl">
          <div className="flex items-center mb-4">
            <Clock className="w-5 h-5 text-gray-300 mr-2" />
            <h3 className="text-white font-medium">Recent Searches</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {searchHistory.map((historyQuery, index) => (
              <button
                key={index}
                onClick={() => handleQuickSearch(historyQuery)}
                className="bg-white bg-opacity-5 text-gray-200 px-3 py-2 rounded-lg text-sm hover:bg-opacity-10 transition-colors flex items-center"
              >
                <Search className="w-3 h-3 mr-2" />
                {historyQuery}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Search Results */}
      {searchResults && (
        <div className="glass-effect p-8 rounded-2xl">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-2xl font-bold text-white">
              Search Results
            </h3>
            <div className="text-sm text-gray-300">
              {searchResults.total_found} files found in {searchResults.search_time}s
            </div>
          </div>

          {searchResults.results.length > 0 ? (
            <div className="space-y-4">
              {searchResults.results.map((file, index) => (
                <div
                  key={index}
                  className="bg-white bg-opacity-5 p-4 rounded-lg hover:bg-opacity-10 transition-colors"
                >
                  <div className="flex items-start space-x-4">
                    <div className="text-2xl">
                      {getCategoryIcon(file.category)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <h4 className="text-white font-medium truncate">
                          {file.filename}
                        </h4>
                        <div className="flex items-center">
                          <Star className="w-4 h-4 text-yellow-400 mr-1" />
                          <span className="text-sm text-gray-300">
                            {file.relevance_score}
                          </span>
                        </div>
                      </div>
                      <p className="text-gray-400 text-sm mb-2 truncate">
                        📁 {file.path}
                      </p>
                      <div className="flex items-center space-x-4 text-xs text-gray-500">
                        <span>{formatFileSize(file.size)}</span>
                        <span>{file.category}</span>
                        <span>{new Date(file.modified).toLocaleDateString()}</span>
                      </div>
                    </div>
                    <button className="text-blue-400 hover:text-blue-300 p-2">
                      <Folder className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <File className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-white font-medium mb-2">No files found</h3>
              <p className="text-gray-400">
                Try a different search query or check your spelling
              </p>
            </div>
          )}
        </div>
      )}

      {/* Search Tips */}
      <div className="glass-effect p-6 rounded-2xl">
        <h3 className="text-white font-medium mb-4">Search Tips</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-300">
          <div>
            <h4 className="text-white font-medium mb-2">Natural Language</h4>
            <ul className="space-y-1">
              <li>• "find my photos from last week"</li>
              <li>• "show me large video files"</li>
              <li>• "recent documents"</li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-medium mb-2">File Types</h4>
            <ul className="space-y-1">
              <li>• "music files" or "audio"</li>
              <li>• "code" or "programming files"</li>
              <li>• "images" or "pictures"</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;