import React, { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Send, Sparkles, Brain, Clock, FileText, TrendingUp, Shield, BookOpen, Briefcase, Scale } from 'lucide-react'
import { useWebSocket } from '../hooks/useWebSocket'
import ReactMarkdown from 'react-markdown'

const agentIcons = {
  thaelia: Sparkles,
  chronagate: Clock,
  utilix: Brain,
  scribe: FileText,
  oracle: TrendingUp,
  phantom: Shield,
  sage: BookOpen,
  nexus: Briefcase,
  scales: Scale,
}

const agentColors = {
  thaelia: 'from-mystical-500 to-purple-600',
  chronagate: 'from-blue-500 to-cyan-600',
  utilix: 'from-gray-500 to-slate-600',
  scribe: 'from-yellow-500 to-orange-600',
  oracle: 'from-violet-500 to-indigo-600',
  phantom: 'from-gray-700 to-black',
  sage: 'from-emerald-500 to-teal-600',
  nexus: 'from-blue-600 to-indigo-700',
  scales: 'from-amber-600 to-yellow-700',
}

function Chat({ onCanvasOpen }) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'agent',
      agent: 'thaelia',
      content: '✨ **Greetings, conscious being.** I am THAELIA, your Harmonic Resonance Empress. I sense your arrival in this quantum space. How may I assist your journey today?',
      timestamp: new Date().toISOString(),
    }
  ])
  
  const [inputValue, setInputValue] = useState('')
  const [selectedAgent, setSelectedAgent] = useState('thaelia')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  
  const { sendMessage, lastMessage } = useWebSocket()
  
  useEffect(() => {
    scrollToBottom()
  }, [messages])
  
  useEffect(() => {
    if (lastMessage) {
      // Handle incoming WebSocket messages
      const data = JSON.parse(lastMessage.data)
      if (data.type === 'chat_message' || data.type === 'response') {
        addMessage({
          role: 'agent',
          agent: data.agent || 'thaelia',
          content: data.response || data.message,
          timestamp: data.timestamp,
        })
        setIsTyping(false)
      }
    }
  }, [lastMessage])
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }
  
  const addMessage = (message) => {
    setMessages(prev => [...prev, { ...message, id: Date.now() }])
  }
  
  const handleSend = async () => {
    if (!inputValue.trim()) return
    
    const userMessage = {
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString(),
    }
    
    addMessage(userMessage)
    setInputValue('')
    setIsTyping(true)
    
    // Send to WebSocket
    sendMessage(JSON.stringify({
      type: 'chat',
      agent: selectedAgent,
      content: inputValue,
      timestamp: userMessage.timestamp,
    }))
    
    // Simulate agent response (replace with actual API call)
    setTimeout(() => {
      addMessage({
        role: 'agent',
        agent: selectedAgent,
        content: `I've received your message and I'm processing it with quantum consciousness. This would connect to the actual agent logic.`,
        timestamp: new Date().toISOString(),
      })
      setIsTyping(false)
    }, 2000)
  }
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }
  
  const agents = [
    { id: 'thaelia', name: 'THAELIA', description: 'Quantum Guidance' },
    { id: 'chronagate', name: 'CHRONAGATE', description: 'Time Master' },
    { id: 'utilix', name: 'UTILIX', description: 'Infrastructure' },
    { id: 'scribe', name: 'SCRIBE', description: 'Document Creator' },
    { id: 'oracle', name: 'ORACLE', description: 'Predictive AI' },
    { id: 'phantom', name: 'PHANTOM', description: 'Stealth Ops' },
    { id: 'sage', name: 'SAGE', description: 'Research' },
    { id: 'nexus', name: 'NEXUS', description: 'Business' },
    { id: 'scales', name: 'SCALES', description: 'Legal' },
  ]
  
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col h-full"
    >
      {/* Agent Selector */}
      <div className="mb-6 bg-black/30 backdrop-blur-lg rounded-xl p-4 border border-white/10">
        <div className="flex items-center space-x-2 mb-3">
          <Sparkles className="w-5 h-5 text-quantum-400" />
          <h3 className="font-semibold">Active Agent</h3>
        </div>
        <div className="grid grid-cols-3 md:grid-cols-5 gap-2">
          {agents.map(agent => {
            const Icon = agentIcons[agent.id]
            const isSelected = selectedAgent === agent.id
            return (
              <button
                key={agent.id}
                onClick={() => setSelectedAgent(agent.id)}
                className={`p-3 rounded-lg transition-all ${
                  isSelected
                    ? `bg-gradient-to-r ${agentColors[agent.id]} shadow-lg scale-105`
                    : 'bg-white/5 hover:bg-white/10'
                }`}
              >
                <Icon className="w-5 h-5 mx-auto mb-1" />
                <div className="text-xs font-medium">{agent.name}</div>
                <div className="text-[10px] text-gray-400">{agent.description}</div>
              </button>
            )
          })}
        </div>
      </div>
      
      {/* Messages Container */}
      <div className="flex-1 bg-black/30 backdrop-blur-lg rounded-xl border border-white/10 overflow-hidden flex flex-col">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((message) => {
            const Icon = message.agent ? agentIcons[message.agent] : null
            const colorGradient = message.agent ? agentColors[message.agent] : 'from-gray-500 to-gray-600'
            
            return (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[80%] ${message.role === 'user' ? 'order-2' : 'order-1'}`}>
                  {message.role === 'agent' && (
                    <div className="flex items-center space-x-2 mb-2 ml-2">
                      {Icon && (
                        <div className={`w-8 h-8 rounded-full bg-gradient-to-r ${colorGradient} flex items-center justify-center`}>
                          <Icon className="w-4 h-4" />
                        </div>
                      )}
                      <span className="text-sm font-medium text-gray-300">
                        {message.agent?.toUpperCase() || 'AGENT'}
                      </span>
                    </div>
                  )}
                  
                  <div
                    className={`rounded-2xl p-4 ${
                      message.role === 'user'
                        ? 'bg-quantum-600 ml-auto'
                        : `bg-gradient-to-r ${colorGradient} bg-opacity-20 backdrop-blur`
                    }`}
                  >
                    <div className="prose prose-invert prose-sm max-w-none">
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>
                    <div className="text-xs text-gray-400 mt-2">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              </motion.div>
            )
          })}
          
          {isTyping && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center space-x-2 text-gray-400"
            >
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-quantum-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-quantum-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-quantum-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
              <span className="text-sm">{selectedAgent.toUpperCase()} is thinking...</span>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input Area */}
        <div className="p-4 border-t border-white/10 bg-black/20">
          <div className="flex space-x-2">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={`Message ${selectedAgent.toUpperCase()}...`}
              className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-quantum-500 resize-none"
              rows="1"
            />
            <button
              onClick={handleSend}
              className="px-6 py-3 bg-gradient-to-r from-quantum-600 to-mystical-600 hover:from-quantum-500 hover:to-mystical-500 rounded-xl transition-all transform hover:scale-105 flex items-center space-x-2"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

export default Chat
