import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { Sparkles, Clock, Brain, FileText, TrendingUp, Shield, BookOpen, Briefcase, Scale } from 'lucide-react'
import { useThaleOSStore } from '../store/thaleosStore'
import { useAuthStore } from '../store/authStore'

const AGENT_ICONS = {
  thaelia:    { icon: Sparkles, color: 'from-mystical-500 to-purple-600' },
  chronagate: { icon: Clock,    color: 'from-blue-500 to-cyan-600' },
  utilix:     { icon: Brain,    color: 'from-gray-500 to-slate-600' },
  scribe:     { icon: FileText, color: 'from-yellow-500 to-orange-600' },
  oracle:     { icon: TrendingUp, color: 'from-violet-500 to-indigo-600' },
  phantom:    { icon: Shield,   color: 'from-gray-700 to-slate-900' },
  sage:       { icon: BookOpen, color: 'from-emerald-500 to-teal-600' },
  nexus:      { icon: Briefcase, color: 'from-blue-600 to-indigo-700' },
  scales:     { icon: Scale,    color: 'from-amber-600 to-yellow-700' },
}

const FLAG_LABELS = {
  can_execute_code:   { label: 'Execute Code', color: 'bg-red-900/60 text-red-300 border-red-700' },
  can_write_files:    { label: 'Write Files',  color: 'bg-orange-900/60 text-orange-300 border-orange-700' },
  requires_admin:     { label: 'Admin Only',   color: 'bg-purple-900/60 text-purple-300 border-purple-700' },
  can_search_web:     { label: 'Web Search',   color: 'bg-blue-900/60 text-blue-300 border-blue-700' },
  can_export_documents: { label: 'Export Docs', color: 'bg-green-900/60 text-green-300 border-green-700' },
}

function CapabilityBadge({ flagKey }) {
  const def = FLAG_LABELS[flagKey]
  if (!def) return null
  return (
    <span className={`text-xs border rounded px-2 py-0.5 ${def.color}`}>
      {def.label}
    </span>
  )
}

function Agents() {
  const { agents, fetchAgents, invokeAgent } = useThaleOSStore()
  const { user } = useAuthStore()

  useEffect(() => {
    fetchAgents()
  }, [])

  const handleInvoke = async (agentId, requiresAdmin) => {
    if (requiresAdmin && user?.role !== 'admin') {
      alert('This agent requires admin role.')
      return
    }
    try {
      await invokeAgent(agentId, 'Hello, introduce yourself.')
    } catch (e) {
      console.error(e)
    }
  }

  // Fall back to hardcoded list if API hasn't loaded yet
  const displayAgents = agents?.length > 0 ? agents : Object.keys(AGENT_ICONS).map(id => ({ id }))

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="space-y-6"
    >
      <h1 className="text-2xl font-display font-bold">Quantum Agents</h1>
      <div className="grid grid-cols-1 gap-4">
        {displayAgents.map((agent) => {
          const meta = AGENT_ICONS[agent.id] || { icon: Sparkles, color: 'from-gray-500 to-gray-700' }
          const Icon = meta.icon
          const flags = agent.capability_flags || {}
          const activeFlags = Object.entries(flags).filter(([, v]) => v).map(([k]) => k)
          const requiresAdmin = flags.requires_admin

          return (
            <motion.div
              key={agent.id}
              whileHover={{ scale: 1.01 }}
              className="bg-black/30 backdrop-blur-lg rounded-xl p-5 border border-white/10 flex items-start space-x-4"
            >
              <div className={`w-14 h-14 rounded-xl bg-gradient-to-r ${meta.color} flex items-center justify-center flex-shrink-0`}>
                <Icon className="w-7 h-7" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-semibold">{agent.display_name || agent.id.toUpperCase()}</div>
                <div className="text-sm text-gray-400">{agent.role || ''}</div>
                {agent.description && (
                  <div className="text-xs text-gray-500 mt-1 truncate">{agent.description}</div>
                )}

                {/* Capability flag badges */}
                {activeFlags.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {activeFlags.map(flag => (
                      <CapabilityBadge key={flag} flagKey={flag} />
                    ))}
                  </div>
                )}

                {/* Tool chips */}
                {agent.tools?.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {agent.tools.map(t => (
                      <span key={t} className="text-xs bg-white/5 border border-white/10 rounded px-2 py-0.5 text-gray-400">
                        {t.replace(/_/g, ' ')}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex flex-col items-end gap-2 flex-shrink-0">
                {agent.status === 'standby' && (
                  <span className="text-xs text-yellow-400 border border-yellow-700 rounded px-2 py-0.5">standby</span>
                )}
                <button
                  onClick={() => handleInvoke(agent.id, requiresAdmin)}
                  disabled={requiresAdmin && user?.role !== 'admin'}
                  className="px-4 py-2 bg-quantum-600 hover:bg-quantum-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-lg text-sm transition-colors"
                  title={requiresAdmin && user?.role !== 'admin' ? 'Requires admin role' : ''}
                >
                  Invoke
                </button>
              </div>
            </motion.div>
          )
        })}
      </div>
    </motion.div>
  )
}

export default Agents
