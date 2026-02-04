import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LandingPage } from './pages/LandingPage';
import { Dashboard } from './pages/Dashboard';
import { AppLayout } from './components/layout/AppLayout';
import './index.css';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={
          <AppLayout>
            <Dashboard />
          </AppLayout>
        } />
        <Route path="/playground" element={
          <AppLayout>
            <div className="text-center py-20">
              <h1 className="text-4xl font-bold gradient-text mb-4">Playground Coming Soon</h1>
              <p className="text-slate-400">Interactive VLSI and Digital Electronics simulations will be available here.</p>
            </div>
          </AppLayout>
        } />
        <Route path="/missions" element={
          <AppLayout>
            <div className="text-center py-20">
              <h1 className="text-4xl font-bold gradient-text mb-4">Missions Coming Soon</h1>
              <p className="text-slate-400">Structured learning paths and challenges will be available here.</p>
            </div>
          </AppLayout>
        } />
        <Route path="/knowledge" element={
          <AppLayout>
            <div className="text-center py-20">
              <h1 className="text-4xl font-bold gradient-text mb-4">Knowledge Base Coming Soon</h1>
              <p className="text-slate-400">Comprehensive engineering resources will be available here.</p>
            </div>
          </AppLayout>
        } />
        <Route path="/clan" element={
          <AppLayout>
            <div className="text-center py-20">
              <h1 className="text-4xl font-bold gradient-text mb-4">Clan System Coming Soon</h1>
              <p className="text-slate-400">Collaborative features and team challenges will be available here.</p>
            </div>
          </AppLayout>
        } />
        <Route path="/settings" element={
          <AppLayout>
            <div className="text-center py-20">
              <h1 className="text-4xl font-bold gradient-text mb-4">Settings Coming Soon</h1>
              <p className="text-slate-400">Personalization options will be available here.</p>
            </div>
          </AppLayout>
        } />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
