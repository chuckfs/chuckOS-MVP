import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { useAuth } from '../context/AuthContext';
import { fileAPI } from '../services/api';
import { Search, Zap, Upload, BarChart3, Sparkles, TrendingUp, FileText, Image, Music, Video } from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();

  // Fetch insights
  const { data: insights, isLoading: insightsLoading } = useQuery(
    'insights',
    fileAPI.getInsights,
    {
      refetchOnWindowFocus: false,
    }
  );

  const features = [
    {
      icon: Search,
      title: 'Smart Search',
      description: 'Find files with natural language like "find my photos from last week"',
      action: 'Start Searching',
      href: '/search',
      gradient: 'from-blue-400 to-blue-600'
    },
    {
      icon: BarChart3,
      title: 'File Analysis',
      description: 'Get comprehensive insights about your file organization patterns',
      action: 'Analyze Files',
      href: '/analysis',
      gradient: 'from-purple-400 to-purple-600'
    },
    {
      icon: Zap,
      title: 'Auto Organization',
      description: 'Let AI organize your files based on learned patterns',
      action: 'Coming Soon',
      href: '#',
      gradient: 'from-green-400 to-green-600'
    }
  ];

  const quickStats = [
    {
      label: 'Searches This Month',
      value: user?.searches_this_month || 0,
      icon: Search,
      color: 'text-blue-400'
    },
    {
      label: 'Files Analyzed',
      value: user?.files_analyzed || 0,
      icon: FileText,
      color: 'text-purple-400'
    },
    {
      label: 'Subscription',
      value: user?.subscription_tier?.toUpperCase() || 'FREE',
      icon: Sparkles,
      color: 'text-green-400'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">
          Welcome back to <span className="gradient-text">Jaymi AI</span>
        </h1>
        <p className="text-xl text-gray-200 mb-8">
          Your intelligent file assistant is ready to help you discover, organize, and manage your files with the power of AI.
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {quickStats.map((stat, index) => (
          <div key={index} className="glass-effect p-6 rounded-2xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-300 text-sm mb-1">{stat.label}</p>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
              </div>
              <stat.icon className={`w-8 h-8 ${stat.color}`} />
            </div>
          </div>
        ))}
      </div>

      {/* Main Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {features.map((feature, index) => (
          <div key={index} className="glass-effect p-8 rounded-2xl group hover:scale-105 transition-transform">
            <div className={`w-12 h-12 bg-gradient-to-r ${feature.gradient} rounded-xl flex items-center justify-center mb-6`}>
              <feature.icon className="w-6 h-6 text-white" />
            </div>
            
            <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
            <p className="text-gray-300 mb-6">{feature.description}</p>
            
            <a
              href={feature.href}
              className={`inline-flex items-center px-4 py-2 bg-gradient-to-r ${feature.gradient} text-white rounded-lg hover:shadow-lg transition-all`}
            >
              {feature.action}
            </a>
          </div>
        ))}
      </div>

      {/* Insights Section */}
      {insights && (
        <div className="glass-effect p-8 rounded-2xl">
          <div className="flex items-center mb-6">
            <TrendingUp className="w-6 h-6 text-blue-400 mr-3" />
            <h2 className="text-2xl font-bold text-white">AI Insights</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {insights.insights?.map((insight, index) => (
              <div key={index} className="bg-white bg-opacity-5 p-6 rounded-xl">
                <div className="flex items-start space-x-3">
                  <div className={`w-2 h-2 rounded-full mt-2 ${
                    insight.priority === 'high' ? 'bg-red-400' :
                    insight.priority === 'medium' ? 'bg-yellow-400' : 'bg-green-400'
                  }`}></div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-white mb-2">{insight.title}</h3>
                    <p className="text-gray-300 text-sm">{insight.message}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Getting Started */}
      <div className="glass-effect p-8 rounded-2xl">
        <h2 className="text-2xl font-bold text-white mb-6">Getting Started</h2>
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">1</div>
            <div>
              <h3 className="text-white font-medium">Try Smart Search</h3>
              <p className="text-gray-300 text-sm">Search for files using natural language like "find my documents from yesterday"</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center text-white font-bold text-sm">2</div>
            <div>
              <h3 className="text-white font-medium">Analyze Your Files</h3>
              <p className="text-gray-300 text-sm">Get insights about your file organization and discover optimization opportunities</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white font-bold text-sm">3</div>
            <div>
              <h3 className="text-white font-medium">Upgrade for More</h3>
              <p className="text-gray-300 text-sm">Unlock unlimited searches and advanced features with Pro subscription</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;