import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Clock, Brain, FileText, TrendingUp, Shield, BookOpen, Briefcase, Scale } from 'lucide-react'
import { useThaleOSStore } from '../store/thaleosStore'

const agentDefs = [
  { id: 'thaelia', name: 'THAELIA', role: 'Harmonic Resonance Empress', icon: Sparkles, color: 'from-mystical-500 to-purple-600', capabilities: ['guidance', 'wisdom', 'quantum_reasoning', 'empathy'] },
  { id: 'chronagate', name: 'CHRONAGATE', role: 'Time Orchestration Master', icon: Clock, color: 'from-blue-500 to-cyan-600', capabilities: ['scheduling', 'time_management', 'task_breakdown', 'calendar_sync'] },
  { id: 'utilix', name: 'UTILIX', role: 'Infrastructure Specialist', icon: Brain, color: 'from-gray-500 to-slate-600', capabilities: ['deployment', 'file_management', 'configuration', 'system_admin'] },
  { id: 'scribe', name: 'SCRIBE', role: 'Professional Document Creator', icon: FileText, color: 'from-yellow-500 to-orange-600', capabilities: ['writing', 'documentation', 'social_media', 'branding'] },
  { id: 'oracle', name: 'ORACLE', role: 'Predictive Intelligence', icon: TrendingUp, color: 'from-violet-500 to-indigo-600', capabilities: ['prediction', 'analysis', 'financial_modeling', 'strategic_planning'] },
  { id: 'phantom', name: 'PHANTOM', role: 'Stealth Operations Specialist', icon: Shield, color: 'from-gray-700 to-slate-900', capabilities: ['background_ops', 'security_research', 'ethical_hacking', 'stealth'] },
  { id: 'sage', name: 'SAGE', role: 'Research & Knowledge Synthesis', icon: BookOpen, color: 'from-emerald-500 to-teal-600', capabilities: ['research', 'synthesis', 'academic_writing', 'analysis'] },
  { id: 'nexus', name: 'NEXUS', role: 'Financial & Business Intelligence', icon: Briefcase, color: 'from-blue-600 to-indigo-700', capabilities: ['financial_analysis', 'business_strategy', 'market_research', 'planning'] },
  { id: 'scales', name: 'SCALES', role: 'Legal Intelligence', icon: Scale, color: 'from-amber-600 to-yellow-700', capabilities: ['legal_drafting', 'contract_review', 'litigation_prep', 'legal_research'] },
]

function Agents() {
  const { invokeAgent } = useThaleOSStore()

  const handleInvoke = async (agentId) => {
    try {
      await invokeAgent(agentId, 'Hello, introduce yourself.')
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="space-y-6"
    >
      <h1 className="text-2xl font-display font-bold">Quantum Agents</h1>
      <div className="grid grid-cols-1 gap-4">
        {agentDefs.map((agent) => {
          const Icon = agent.icon
          return (
            <motion.div
              key={agent.id}
              whileHover={{ scale: 1.01 }}
              className="bg-black/30 backdrop-blur-lg rounded-xl p-5 border border-white/10 flex items-center space-x-4"
            >
              <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${agent.color} flex items-center justify-center flex-shrink-0`}>
                <Icon className="w-7 h-7" />
              </div>
              <div className="flex-1">
                <div className="font-semibold">{agent.name}</div>
                <div className="text-sm text-gray-400">{agent.role}</div>
                <div className="flex flex-wrap gap-1 mt-2">
                  {agent.capabilities.map(cap => (
                    <span key={cap} className="text-xs bg-white/5 border border-white/10 rounded px-2 py-0.5 text-gray-300">
                      {cap.replace('_', ' ')}
                    </span>
                  ))}
                </div>
              </div>
              <button
                onClick={() => handleInvoke(agent.id)}
                className="px-4 py-2 bg-quantum-600 hover:bg-quantum-500 rounded-lg text-sm transition-colors flex-shrink-0"
              >
                Invoke
              </button>
            </motion.div>
          )
        })}
      </div>
    </motion.div>
  )
}

export default Agents
