import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Sparkles, Clock, Brain, FileText, TrendingUp, Shield, BookOpen, Briefcase, Scale, Activity, Zap, Users } from 'lucide-react'
import { useThaleOSStore } from '../store/thaleosStore'

const agentCards = [
  { id: 'thaelia', name: 'THAELIA', role: 'Harmonic Resonance Empress', icon: Sparkles, color: 'from-mystical-500 to-purple-600', status: 'active' },
  { id: 'chronagate', name: 'CHRONAGATE', role: 'Time Orchestration Master', icon: Clock, color: 'from-blue-500 to-cyan-600', status: 'active' },
  { id: 'utilix', name: 'UTILIX', role: 'Infrastructure Specialist', icon: Brain, color: 'from-gray-500 to-slate-600', status: 'active' },
  { id: 'scribe', name: 'SCRIBE', role: 'Document Creator', icon: FileText, color: 'from-yellow-500 to-orange-600', status: 'active' },
  { id: 'oracle', name: 'ORACLE', role: 'Predictive Intelligence', icon: TrendingUp, color: 'from-violet-500 to-indigo-600', status: 'active' },
  { id: 'phantom', name: 'PHANTOM', role: 'Stealth Operations', icon: Shield, color: 'from-gray-700 to-slate-900', status: 'standby' },
  { id: 'sage', name: 'SAGE', role: 'Research Expert', icon: BookOpen, color: 'from-emerald-500 to-teal-600', status: 'active' },
  { id: 'nexus', name: 'NEXUS', role: 'Business Analyst', icon: Briefcase, color: 'from-blue-600 to-indigo-700', status: 'active' },
  { id: 'scales', name: 'SCALES', role: 'Legal Intelligence', icon: Scale, color: 'from-amber-600 to-yellow-700', status: 'active' },
]

function Dashboard() {
  const { systemStatus, fetchSystemStatus } = useThaleOSStore()

  useEffect(() => {
    fetchSystemStatus()
  }, [])

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="text-center py-6">
        <motion.h1
          className="text-4xl font-display font-bold bg-clip-text text-transparent bg-quantum-gradient mb-2"
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
        >
          ThaleOS Quantum Intelligence
        </motion.h1>
        <p className="text-gray-400">9 Quantum Agents • Real-time AI Orchestration</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Agents Online', value: '9', icon: Users, color: 'text-quantum-400' },
          { label: 'Quantum Coherence', value: 'Optimal', icon: Zap, color: 'text-harmonic-400' },
          { label: 'Resonance', value: '432 Hz', icon: Activity, color: 'text-mystical-400' },
        ].map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="bg-black/30 backdrop-blur-lg rounded-xl p-4 border border-white/10 flex items-center space-x-3">
            <Icon className={`w-8 h-8 ${color}`} />
            <div>
              <div className="text-xl font-bold">{value}</div>
              <div className="text-xs text-gray-400">{label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Agents Grid */}
      <div>
        <h2 className="text-lg font-semibold mb-4 flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-quantum-400" />
          <span>Quantum Agents</span>
        </h2>
        <div className="grid grid-cols-3 gap-3">
          {agentCards.map((agent) => {
            const Icon = agent.icon
            return (
              <Link key={agent.id} to="/chat">
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="bg-black/30 backdrop-blur-lg rounded-xl p-4 border border-white/10 hover:border-quantum-500/50 transition-all cursor-pointer"
                >
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-r ${agent.color} flex items-center justify-center mb-3`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div className="font-semibold text-sm">{agent.name}</div>
                  <div className="text-xs text-gray-400 mt-1">{agent.role}</div>
                  <div className={`mt-2 flex items-center space-x-1 text-xs ${agent.status === 'active' ? 'text-harmonic-400' : 'text-yellow-400'}`}>
                    <div className={`w-1.5 h-1.5 rounded-full ${agent.status === 'active' ? 'bg-harmonic-400 animate-pulse' : 'bg-yellow-400'}`}></div>
                    <span className="capitalize">{agent.status}</span>
                  </div>
                </motion.div>
              </Link>
            )
          })}
        </div>
      </div>
    </motion.div>
  )
}

export default Dashboard
