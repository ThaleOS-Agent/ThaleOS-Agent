import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Calendar, Plus, Clock } from 'lucide-react'
import { useThaleOSStore } from '../store/thaleosStore'

function Schedule() {
  const { schedule, fetchSchedule, scheduleTask } = useThaleOSStore()
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', description: '', start_time: '', duration: 60, priority: 'medium' })

  useEffect(() => {
    fetchSchedule()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    await scheduleTask(form)
    setShowForm(false)
    setForm({ title: '', description: '', start_time: '', duration: 60, priority: 'medium' })
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="space-y-6"
    >
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-display font-bold">Schedule</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center space-x-2 px-4 py-2 bg-quantum-600 hover:bg-quantum-500 rounded-lg text-sm transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Add Task</span>
        </button>
      </div>

      {showForm && (
        <motion.form
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          onSubmit={handleSubmit}
          className="bg-black/30 backdrop-blur-lg rounded-xl p-5 border border-white/10 space-y-4"
        >
          <h3 className="font-semibold">New Scheduled Task</h3>
          <input
            type="text"
            placeholder="Task title"
            value={form.title}
            onChange={e => setForm({ ...form, title: e.target.value })}
            className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-quantum-500"
            required
          />
          <input
            type="datetime-local"
            value={form.start_time}
            onChange={e => setForm({ ...form, start_time: e.target.value })}
            className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-quantum-500"
            required
          />
          <div className="flex space-x-2">
            <button type="submit" className="px-4 py-2 bg-quantum-600 hover:bg-quantum-500 rounded-lg text-sm transition-colors">
              Schedule
            </button>
            <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-sm transition-colors">
              Cancel
            </button>
          </div>
        </motion.form>
      )}

      {schedule.length === 0 ? (
        <div className="text-center py-20 text-gray-500">
          <Calendar className="w-16 h-16 mx-auto mb-4 opacity-20" />
          <p className="text-lg">No tasks scheduled today</p>
          <p className="text-sm mt-1">CHRONAGATE is ready to optimize your time</p>
        </div>
      ) : (
        <div className="space-y-3">
          {schedule.map((task, i) => (
            <div key={i} className="bg-black/30 backdrop-blur-lg rounded-xl p-4 border border-white/10 flex items-center space-x-4">
              <Clock className="w-6 h-6 text-blue-400 flex-shrink-0" />
              <div>
                <div className="font-medium">{task.title}</div>
                <div className="text-xs text-gray-400">{task.start_time}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  )
}

export default Schedule
