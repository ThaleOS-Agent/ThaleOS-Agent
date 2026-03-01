/**
 * ThaleOS Auth Store
 * JWT tokens stored in-memory (not localStorage) for XSS safety.
 * Tokens survive page navigation but NOT hard refresh — user re-logs in.
 */
import { create } from 'zustand'
import axios from 'axios'

const API_URL = 'http://localhost:8099'

// Module-level token (not in React state — never serialized to storage)
let _accessToken = null

export function getAccessToken() {
  return _accessToken
}

// Axios interceptor: attach token to every request
axios.interceptors.request.use((config) => {
  if (_accessToken && !config._noAuth) {
    config.headers.Authorization = `Bearer ${_accessToken}`
  }
  return config
})

// Axios interceptor: auto-refresh on 401
axios.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const { refreshToken, refreshAccessToken, logout } = useAuthStore.getState()
      if (refreshToken) {
        try {
          await refreshAccessToken()
          original.headers.Authorization = `Bearer ${_accessToken}`
          return axios(original)
        } catch {
          logout()
        }
      } else {
        logout()
      }
    }
    return Promise.reject(error)
  }
)

export const useAuthStore = create((set, get) => ({
  user: null,
  refreshToken: null,     // stored in state (memory only)
  isLoading: false,
  error: null,

  register: async (username, email, password) => {
    set({ isLoading: true, error: null })
    try {
      const res = await axios.post(`${API_URL}/auth/register`, { username, email, password }, { _noAuth: true })
      _accessToken = res.data.access_token
      set({ user: res.data.user, refreshToken: res.data.refresh_token, isLoading: false })
    } catch (err) {
      set({ error: err.response?.data?.detail || 'Registration failed', isLoading: false })
      throw err
    }
  },

  login: async (username, password) => {
    set({ isLoading: true, error: null })
    try {
      const res = await axios.post(`${API_URL}/auth/login`, { username, password }, { _noAuth: true })
      _accessToken = res.data.access_token
      set({ user: res.data.user, refreshToken: res.data.refresh_token, isLoading: false })
    } catch (err) {
      set({ error: err.response?.data?.detail || 'Login failed', isLoading: false })
      throw err
    }
  },

  refreshAccessToken: async () => {
    const { refreshToken } = get()
    if (!refreshToken) throw new Error('No refresh token')
    const res = await axios.post(`${API_URL}/auth/refresh`, { refresh_token: refreshToken }, { _noAuth: true })
    _accessToken = res.data.access_token
  },

  logout: async () => {
    const { refreshToken } = get()
    if (refreshToken) {
      try {
        await axios.post(`${API_URL}/auth/logout`, { refresh_token: refreshToken }, { _noAuth: true })
      } catch { /* ignore */ }
    }
    _accessToken = null
    set({ user: null, refreshToken: null, error: null })
  },

  clearError: () => set({ error: null }),
}))
