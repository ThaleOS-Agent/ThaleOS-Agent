import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Calendar as CalendarIcon, Plus, ExternalLink, AlertTriangle, CheckCircle, X } from 'lucide-react'
import axios from 'axios'

const API_URL = 'http://localhost:8099/api'

function formatDateTime(iso) {
  if (!iso) return ''
  return new Date(iso).toLocaleString(undefined, {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit',
  })
}

function EventCard({ event, onDelete }) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-4 flex items-start justify-between gap-3">
      <div className="flex-1 min-w-0">
        <div className="font-medium truncate">{event.title}</div>
        <div className="text-sm text-gray-400 mt-0.5">
          {formatDateTime(event.start)} — {formatDateTime(event.end)}
        </div>
        {event.location && (
          <div className="text-xs text-gray-500 mt-1">📍 {event.location}</div>
        )}
        {event.description && (
          <div className="text-xs text-gray-500 mt-1 line-clamp-2">{event.description}</div>
        )}
      </div>
      <button
        onClick={() => onDelete(event.id)}
        className="p-1 text-gray-600 hover:text-red-400 transition-colors flex-shrink-0"
        title="Delete event"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  )
}

function NewEventModal({ onClose, onCreated }) {
  const [form, setForm] = useState({ title: '', start: '', end: '', description: '', location: '' })
  const [conflicts, setConflicts] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const handleSubmit = async (force = false) => {
    setLoading(true)
    setError(null)
    try {
      await axios.post(`${API_URL}/calendar/events`, { ...form, skip_conflict_check: force })
      onCreated()
      onClose()
    } catch (err) {
      if (err.response?.status === 409) {
        setConflicts(err.response.data.detail?.conflicts || [])
      } else {
        setError(err.response?.data?.detail || 'Failed to create event')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-slate-900 border border-white/20 rounded-2xl p-6 w-full max-w-md"
      >
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">New Event</h2>
          <button onClick={onClose} className="p-1 hover:bg-white/10 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        {conflicts ? (
          <div>
            <div className="flex items-center gap-2 text-yellow-400 mb-3">
              <AlertTriangle className="w-5 h-5" />
              <span className="font-medium">Scheduling Conflict</span>
            </div>
            <p className="text-sm text-gray-400 mb-3">
              {conflicts.length} event{conflicts.length > 1 ? 's' : ''} overlap with this time slot:
            </p>
            <div className="space-y-2 mb-4">
              {conflicts.map(c => (
                <div key={c.id} className="text-sm bg-yellow-900/20 border border-yellow-700/30 rounded-lg px-3 py-2">
                  <div className="font-medium text-yellow-300">{c.title}</div>
                  <div className="text-xs text-gray-400">{formatDateTime(c.start)} — {formatDateTime(c.end)}</div>
                </div>
              ))}
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setConflicts(null)}
                className="flex-1 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-sm transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => handleSubmit(true)}
                disabled={loading}
                className="flex-1 py-2 bg-yellow-600 hover:bg-yellow-500 disabled:opacity-50 rounded-lg text-sm transition-colors"
              >
                Schedule Anyway
              </button>
            </div>
          </div>
        ) : (
          <form onSubmit={(e) => { e.preventDefault(); handleSubmit() }} className="space-y-3">
            {[
              { name: 'title', label: 'Title', type: 'text', required: true },
              { name: 'start', label: 'Start', type: 'datetime-local', required: true },
              { name: 'end', label: 'End', type: 'datetime-local', required: true },
              { name: 'location', label: 'Location', type: 'text', required: false },
              { name: 'description', label: 'Description', type: 'text', required: false },
            ].map(f => (
              <div key={f.name}>
                <label className="block text-xs text-gray-400 mb-1">{f.label}</label>
                <input
                  name={f.name}
                  type={f.type}
                  required={f.required}
                  value={form[f.name]}
                  onChange={handleChange}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"
                />
              </div>
            ))}
            {error && (
              <div className="text-red-400 text-sm bg-red-900/20 border border-red-500/30 rounded-lg px-3 py-2">
                {typeof error === 'string' ? error : JSON.stringify(error)}
              </div>
            )}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 rounded-lg text-sm font-medium transition-colors"
            >
              {loading ? 'Creating...' : 'Create Event'}
            </button>
          </form>
        )}
      </motion.div>
    </div>
  )
}

export default function Calendar() {
  const [status, setStatus] = useState(null)
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [days, setDays] = useState(7)

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_URL}/calendar/status`)
      setStatus(res.data)
    } catch { setStatus({ connected: false }) }
  }

  const fetchEvents = async () => {
    try {
      const res = await axios.get(`${API_URL}/calendar/events?days=${days}`)
      setEvents(res.data.events || [])
    } catch { setEvents([]) }
  }

  useEffect(() => {
    fetchStatus().then(() => setLoading(false))
    // Check for OAuth callback result in URL
    const params = new URLSearchParams(window.location.search)
    if (params.get('calendar_connected')) {
      fetchStatus()
      window.history.replaceState({}, '', window.location.pathname)
    }
  }, [])

  useEffect(() => {
    if (status?.connected) fetchEvents()
  }, [status, days])

  const handleConnect = async () => {
    try {
      const res = await axios.get(`${API_URL}/calendar/connect`)
      window.location.href = res.data.auth_url
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to start Google OAuth')
    }
  }

  const handleDelete = async (eventId) => {
    if (!confirm('Delete this event from Google Calendar?')) return
    try {
      await axios.delete(`${API_URL}/calendar/events/${eventId}`)
      setEvents(e => e.filter(ev => ev.id !== eventId))
    } catch (err) {
      alert(err.response?.data?.detail || 'Delete failed')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        Loading calendar...
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display font-bold flex items-center gap-2">
          <CalendarIcon className="w-6 h-6 text-blue-400" />
          Calendar
        </h1>
        {status?.connected && (
          <div className="flex items-center gap-3">
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="bg-white/10 border border-white/20 rounded-lg px-3 py-1.5 text-sm text-white"
            >
              {[3, 7, 14, 30].map(d => (
                <option key={d} value={d}>{d} days</option>
              ))}
            </select>
            <button
              onClick={() => setShowModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm transition-colors"
            >
              <Plus className="w-4 h-4" />
              New Event
            </button>
          </div>
        )}
      </div>

      {!status?.connected ? (
        <div className="bg-black/30 border border-white/10 rounded-2xl p-10 text-center">
          <CalendarIcon className="w-14 h-14 mx-auto mb-4 text-blue-400 opacity-60" />
          <h2 className="text-xl font-semibold mb-2">Connect Google Calendar</h2>
          <p className="text-gray-400 text-sm mb-6 max-w-sm mx-auto">
            Sync your calendar events, check for conflicts, and let ChronaGate help you schedule intelligently.
          </p>
          <button
            onClick={handleConnect}
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-500 rounded-xl font-medium transition-colors"
          >
            <ExternalLink className="w-5 h-5" />
            Connect with Google
          </button>
          <p className="text-xs text-gray-600 mt-4">
            Requires GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env
          </p>
        </div>
      ) : (
        <div>
          <div className="flex items-center gap-2 text-sm text-green-400 mb-4">
            <CheckCircle className="w-4 h-4" />
            Google Calendar connected — showing next {days} days
          </div>
          {events.length === 0 ? (
            <div className="bg-black/20 border border-white/10 rounded-xl p-8 text-center text-gray-500">
              No upcoming events in the next {days} days.
            </div>
          ) : (
            <div className="space-y-3">
              {events.map(event => (
                <EventCard key={event.id} event={event} onDelete={handleDelete} />
              ))}
            </div>
          )}
        </div>
      )}

      {showModal && (
        <NewEventModal
          onClose={() => setShowModal(false)}
          onCreated={fetchEvents}
        />
      )}
    </motion.div>
  )
}
