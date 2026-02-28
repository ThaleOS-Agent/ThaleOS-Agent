import React from 'react'
import { motion } from 'framer-motion'
import { Settings as SettingsIcon, Key, Bell, Zap, User } from 'lucide-react'
import { useThaleOSStore } from '../store/thaleosStore'

function Settings() {
  const { user, updateUserPreferences } = useThaleOSStore()

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="space-y-6 max-w-2xl"
    >
      <h1 className="text-2xl font-display font-bold">Settings</h1>

      {/* User Preferences */}
      <div className="bg-black/30 backdrop-blur-lg rounded-xl p-5 border border-white/10 space-y-4">
        <div className="flex items-center space-x-2 mb-4">
          <User className="w-5 h-5 text-quantum-400" />
          <h2 className="font-semibold">User Preferences</h2>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-medium">Notifications</div>
            <div className="text-xs text-gray-400">Receive agent activity alerts</div>
          </div>
          <button
            onClick={() => updateUserPreferences({ notifications: !user.preferences.notifications })}
            className={`w-12 h-6 rounded-full transition-colors ${user.preferences.notifications ? 'bg-quantum-600' : 'bg-white/10'}`}
          >
            <div className={`w-5 h-5 rounded-full bg-white transition-transform mx-0.5 ${user.preferences.notifications ? 'translate-x-6' : 'translate-x-0'}`}></div>
          </button>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <div className="text-sm font-medium">Quantum Resonance</div>
            <div className="text-xs text-gray-400">432Hz frequency synchronization</div>
          </div>
          <button
            onClick={() => updateUserPreferences({ quantumResonance: !user.preferences.quantumResonance })}
            className={`w-12 h-6 rounded-full transition-colors ${user.preferences.quantumResonance ? 'bg-quantum-600' : 'bg-white/10'}`}
          >
            <div className={`w-5 h-5 rounded-full bg-white transition-transform mx-0.5 ${user.preferences.quantumResonance ? 'translate-x-6' : 'translate-x-0'}`}></div>
          </button>
        </div>
      </div>

      {/* API Configuration */}
      <div className="bg-black/30 backdrop-blur-lg rounded-xl p-5 border border-white/10 space-y-4">
        <div className="flex items-center space-x-2 mb-4">
          <Key className="w-5 h-5 text-quantum-400" />
          <h2 className="font-semibold">API Configuration</h2>
        </div>
        <p className="text-sm text-gray-400">Configure API keys in the <code className="text-quantum-300">.env</code> file at the project root.</p>

        {[
          { label: 'Anthropic Claude', key: 'ANTHROPIC_API_KEY' },
          { label: 'OpenAI', key: 'OPENAI_API_KEY' },
          { label: 'Perplexity', key: 'PERPLEXITY_API_KEY' },
        ].map(({ label, key }) => (
          <div key={key} className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
            <div className="text-sm">{label}</div>
            <span className="text-xs bg-white/5 border border-white/10 rounded px-2 py-1 font-mono text-gray-400">{key}</span>
          </div>
        ))}
      </div>

      {/* System Info */}
      <div className="bg-black/30 backdrop-blur-lg rounded-xl p-5 border border-white/10">
        <div className="flex items-center space-x-2 mb-4">
          <Zap className="w-5 h-5 text-quantum-400" />
          <h2 className="font-semibold">System Information</h2>
        </div>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between"><span className="text-gray-400">Version</span><span>v1.0.0 Quantum Awakening</span></div>
          <div className="flex justify-between"><span className="text-gray-400">Backend</span><span>http://localhost:8099</span></div>
          <div className="flex justify-between"><span className="text-gray-400">API Docs</span><span>http://localhost:8099/api/docs</span></div>
        </div>
      </div>
    </motion.div>
  )
}

export default Settings
