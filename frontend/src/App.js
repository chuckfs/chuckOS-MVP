import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';

// Components
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import SearchPage from './components/SearchPage';
import AnalysisPage from './components/AnalysisPage';
import AuthPage from './components/AuthPage';
import PricingPage from './components/PricingPage';

// Context
import { AuthProvider, useAuth } from './context/AuthContext';

// API
import { api } from './services/api';

const queryClient = new QueryClient();

function AppContent() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-effect p-8 rounded-2xl">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto"></div>
          <p className="text-white mt-4 text-center">Loading Jaymi AI...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route 
            path="/" 
            element={user ? <Dashboard /> : <Navigate to="/auth" />} 
          />
          <Route 
            path="/search" 
            element={user ? <SearchPage /> : <Navigate to="/auth" />} 
          />
          <Route 
            path="/analysis" 
            element={user ? <AnalysisPage /> : <Navigate to="/auth" />} 
          />
          <Route 
            path="/auth" 
            element={!user ? <AuthPage /> : <Navigate to="/" />} 
          />
          <Route path="/pricing" element={<PricingPage />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <AppContent />
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(10px)',
                color: 'white',
                border: '1px solid rgba(255, 255, 255, 0.2)',
              },
            }}
          />
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;