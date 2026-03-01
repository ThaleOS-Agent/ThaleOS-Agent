import React, { useEffect, useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Sidebar from './components/Sidebar'
import ProtectedRoute from './components/ProtectedRoute'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import Agents from './pages/Agents'
import Documents from './pages/Documents'
import Schedule from './pages/Schedule'
import Settings from './pages/Settings'
import Login from './pages/Login'
import Calendar from './pages/Calendar'
import Canvas from './components/Canvas'
import SystemTray from './components/SystemTray'
import { useWebSocket } from './hooks/useWebSocket'
import { useThaleOSStore } from './store/thaleosStore'
import { useAuthStore } from './store/authStore'
import './App.css'

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [canvasOpen, setCanvasOpen] = useState(false)
  const [canvasContent, setCanvasContent] = useState(null)

  const { isConnected, connect } = useWebSocket()
  const { systemStatus, fetchSystemStatus } = useThaleOSStore()
  const { user, logout } = useAuthStore()
  
  useEffect(() => {
    // Connect to backend WebSocket
    connect()
    
    // Fetch initial system status
    fetchSystemStatus()
    
    // Check if running in Tauri
    if (window.__TAURI__) {
      console.log('🚀 Running in Tauri native app')
    }
  }, [])
  
  const toggleCanvas = (content = null) => {
    setCanvasOpen(!canvasOpen)
    if (content) setCanvasContent(content)
  }
  
  // Unauthenticated: show only login
  if (!user) {
    return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    )
  }

  return (
    <Router>
      <div className="app-container flex h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden">
        {/* Quantum background effects */}
        <div className="fixed inset-0 opacity-30 pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-quantum-500 rounded-full filter blur-3xl animate-pulse-slow"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-mystical-500 rounded-full filter blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
        </div>

        {/* Sidebar */}
        <Sidebar collapsed={sidebarCollapsed} onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} />

        {/* Main Content */}
        <div className={`flex-1 flex flex-col transition-all duration-300 relative z-10 ${sidebarCollapsed ? 'ml-20' : 'ml-64'}`}>
          {/* Header */}
          <header className="bg-black/30 backdrop-blur-lg border-b border-white/10 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <motion.div
                  className="text-2xl font-display font-bold bg-clip-text text-transparent bg-quantum-gradient"
                  initial={{ opacity: 0, y: -20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  ThaleOS
                </motion.div>
                <div className="flex items-center space-x-2">
                  <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-harmonic-400 animate-pulse' : 'bg-red-500'}`}></div>
                  <span className="text-sm text-gray-300">
                    {isConnected ? 'Quantum Link Active' : 'Reconnecting...'}
                  </span>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <button
                  onClick={() => toggleCanvas()}
                  className="px-4 py-2 bg-quantum-600 hover:bg-quantum-500 rounded-lg transition-colors"
                >
                  Canvas
                </button>
                <SystemTray />
                {/* User badge */}
                <div className="flex items-center space-x-2 border border-white/10 rounded-lg px-3 py-1.5">
                  <span className="text-sm text-gray-300">{user.username}</span>
                  <span className={`text-xs px-1.5 py-0.5 rounded ${user.role === 'admin' ? 'bg-purple-700 text-purple-200' : 'bg-slate-700 text-gray-300'}`}>
                    {user.role}
                  </span>
                  <button
                    onClick={logout}
                    className="text-xs text-gray-500 hover:text-red-400 transition-colors ml-1"
                    title="Sign out"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
          </header>

          {/* Main Routes */}
          <main className="flex-1 overflow-auto p-6">
            <AnimatePresence mode="wait">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/chat" element={<Chat onCanvasOpen={toggleCanvas} />} />
                <Route path="/agents" element={<Agents />} />
                <Route path="/documents" element={<Documents onCanvasOpen={toggleCanvas} />} />
                <Route path="/schedule" element={<Schedule />} />
                <Route path="/calendar" element={<Calendar />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="/login" element={<Navigate to="/" replace />} />
              </Routes>
            </AnimatePresence>
          </main>
        </div>

        {/* Canvas Sidebar */}
        <AnimatePresence>
          {canvasOpen && (
            <Canvas
              content={canvasContent}
              onClose={() => setCanvasOpen(false)}
            />
          )}
        </AnimatePresence>
      </div>
    </Router>
  )
}

export default App
