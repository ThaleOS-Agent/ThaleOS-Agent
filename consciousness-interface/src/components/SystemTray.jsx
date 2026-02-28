import React, { useState } from 'react'
import { Bell } from 'lucide-react'

function SystemTray() {
  const [hasNotifications] = useState(false)

  return (
    <div className="relative">
      <button className="p-2 hover:bg-white/10 rounded-lg transition-colors relative">
        <Bell className="w-5 h-5 text-gray-400" />
        {hasNotifications && (
          <span className="absolute top-1 right-1 w-2 h-2 bg-quantum-400 rounded-full"></span>
        )}
      </button>
    </div>
  )
}

export default SystemTray
