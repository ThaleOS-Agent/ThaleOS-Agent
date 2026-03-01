import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Home, MessageSquare, Users, FileText, Calendar, CalendarDays, Settings, Zap, ChevronLeft, ChevronRight } from 'lucide-react'

const navItems = [
  { path: '/', icon: Home, label: 'Dashboard' },
  { path: '/chat', icon: MessageSquare, label: 'Chat' },
  { path: '/agents', icon: Users, label: 'Agents' },
  { path: '/documents', icon: FileText, label: 'Documents' },
  { path: '/schedule', icon: Calendar, label: 'Schedule' },
  { path: '/calendar', icon: CalendarDays, label: 'Calendar' },
  { path: '/settings', icon: Settings, label: 'Settings' },
]

function Sidebar({ collapsed, onToggle }) {
  const location = useLocation()

  return (
    <motion.div
      className={`fixed left-0 top-0 h-full bg-black/40 backdrop-blur-xl border-r border-white/10 flex flex-col z-20 transition-all duration-300 ${collapsed ? 'w-20' : 'w-64'}`}
      initial={false}
    >
      {/* Logo */}
      <div className="p-4 flex items-center justify-between border-b border-white/10">
        {!collapsed && (
          <div className="flex items-center space-x-2">
            <Zap className="w-6 h-6 text-quantum-400" />
            <span className="font-display font-bold text-quantum-300">ThaleOS</span>
          </div>
        )}
        {collapsed && <Zap className="w-6 h-6 text-quantum-400 mx-auto" />}
        <button
          onClick={onToggle}
          className="p-1 rounded-lg hover:bg-white/10 transition-colors text-gray-400"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map(({ path, icon: Icon, label }) => {
          const isActive = location.pathname === path
          return (
            <Link
              key={path}
              to={path}
              className={`flex items-center space-x-3 px-3 py-3 rounded-lg transition-all ${
                isActive
                  ? 'bg-quantum-600/50 text-white border border-quantum-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
            >
              <Icon className="w-5 h-5 flex-shrink-0" />
              {!collapsed && <span className="text-sm font-medium">{label}</span>}
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-white/10">
        <div className={`flex items-center ${collapsed ? 'justify-center' : 'space-x-3'}`}>
          <div className="w-8 h-8 rounded-full bg-gradient-to-r from-quantum-600 to-mystical-600 flex items-center justify-center text-xs font-bold">
            Q
          </div>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium truncate">Quantum Explorer</div>
              <div className="text-xs text-gray-400">v1.0.0</div>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  )
}

export default Sidebar
