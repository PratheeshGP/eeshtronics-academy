import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { LandingPage } from './pages/LandingPage';
import { Dashboard } from './pages/Dashboard';
import LoginPage from './pages/LoginPage';
import { AppLayout } from './components/layout/AppLayout';
import './index.css';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <AppLayout>
                <Dashboard />
              </AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/playground" element={
            <ProtectedRoute>
              <AppLayout>
                <div className="text-center py-20">
                  <h1 className="text-4xl font-bold gradient-text mb-4">Playground Coming Soon</h1>
                  <p className="text-slate-400">Interactive VLSI and Digital Electronics simulations will be available here.</p>
                </div>
              </AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/missions" element={
            <ProtectedRoute>
              <AppLayout>
                <div className="text-center py-20">
                  <h1 className="text-4xl font-bold gradient-text mb-4">Missions Coming Soon</h1>
                  <p className="text-slate-400">Structured learning paths and challenges will be available here.</p>
                </div>
              </AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/knowledge" element={
            <ProtectedRoute>
              <AppLayout>
                <div className="text-center py-20">
                  <h1 className="text-4xl font-bold gradient-text mb-4">Knowledge Base Coming Soon</h1>
                  <p className="text-slate-400">Comprehensive engineering resources will be available here.</p>
                </div>
              </AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/clan" element={
            <ProtectedRoute>
              <AppLayout>
                <div className="text-center py-20">
                  <h1 className="text-4xl font-bold gradient-text mb-4">Clan System Coming Soon</h1>
                  <p className="text-slate-400">Collaborative features and team challenges will be available here.</p>
                </div>
              </AppLayout>
            </ProtectedRoute>
          } />
          <Route path="/settings" element={
            <ProtectedRoute>
              <AppLayout>
                <div className="text-center py-20">
                  <h1 className="text-4xl font-bold gradient-text mb-4">Settings Coming Soon</h1>
                  <p className="text-slate-400">Personalization options will be available here.</p>
                </div>
              </AppLayout>
            </ProtectedRoute>
          } />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
};

export default App;
