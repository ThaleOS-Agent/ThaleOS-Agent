import { create } from 'zustand'
import axios from 'axios'

const API_URL = 'http://localhost:8099/api'

export const useThaleOSStore = create((set, get) => ({
  // System state
  systemStatus: null,
  agents: [],
  documents: [],
  schedule: [],

  // UI state
  theme: 'dark',
  sidebarCollapsed: false,

  // User state
  user: {
    name: 'Quantum Explorer',
    avatar: null,
    preferences: {
      defaultAgent: 'thaelia',
      notifications: true,
      quantumResonance: true,
    }
  },

  // Actions
  fetchSystemStatus: async () => {
    try {
      const response = await axios.get(`${API_URL}/system/status`)
      set({ systemStatus: response.data })
    } catch (error) {
      console.error('Failed to fetch system status:', error)
    }
  },

  fetchAgents: async () => {
    try {
      const response = await axios.get(`${API_URL}/agents/list`)
      set({ agents: response.data.agents })
    } catch (error) {
      console.error('Failed to fetch agents:', error)
    }
  },

  invokeAgent: async (agentId, task) => {
    try {
      const response = await axios.post(`${API_URL}/agents/invoke`, {
        agent: agentId,
        task: task,
        parameters: {}
      })
      return response.data
    } catch (error) {
      console.error('Failed to invoke agent:', error)
      throw error
    }
  },

  fetchDocuments: async () => {
    try {
      const response = await axios.get(`${API_URL}/documents/list`)
      set({ documents: response.data.documents })
    } catch (error) {
      console.error('Failed to fetch documents:', error)
    }
  },

  createDocument: async (docType, content, metadata) => {
    try {
      const response = await axios.post(`${API_URL}/documents/create`, {
        doc_type: docType,
        content: content,
        metadata: metadata
      })
      get().fetchDocuments()
      return response.data
    } catch (error) {
      console.error('Failed to create document:', error)
      throw error
    }
  },

  fetchSchedule: async () => {
    try {
      const response = await axios.get(`${API_URL}/schedule/today`)
      set({ schedule: response.data.tasks })
    } catch (error) {
      console.error('Failed to fetch schedule:', error)
    }
  },

  scheduleTask: async (task) => {
    try {
      const response = await axios.post(`${API_URL}/schedule/task`, task)
      get().fetchSchedule()
      return response.data
    } catch (error) {
      console.error('Failed to schedule task:', error)
      throw error
    }
  },

  reason: async (query, preferredAgent = null) => {
    try {
      const response = await axios.post(`${API_URL}/reason`, {
        query,
        preferred_agent: preferredAgent,
      })
      return response.data
    } catch (error) {
      console.error('Reasoning pipeline failed:', error)
      throw error
    }
  },

  search: async (query, type = 'web', count = 5) => {
    try {
      const response = await axios.post(`${API_URL}/search`, { query, type, count })
      return response.data
    } catch (error) {
      console.error('Search failed:', error)
      throw error
    }
  },

  sendChat: async (agentId, content) => {
    try {
      const response = await axios.post(`${API_URL}/chat/message`, {
        role: 'user',
        content,
        agent: agentId,
      })
      return response.data
    } catch (error) {
      console.error('Chat failed:', error)
      throw error
    }
  },

  setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
  setTheme: (theme) => set({ theme }),
  updateUserPreferences: (preferences) => set((state) => ({
    user: {
      ...state.user,
      preferences: {
        ...state.user.preferences,
        ...preferences
      }
    }
  })),
}))
