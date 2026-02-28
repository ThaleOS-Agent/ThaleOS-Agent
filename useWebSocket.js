import { useEffect, useRef, useState } from 'react'

const WS_URL = 'ws://localhost:8099/ws/'

export function useWebSocket() {
  const [isConnected, setIsConnected] = useState(false)
  const [lastMessage, setLastMessage] = useState(null)
  const ws = useRef(null)
  const reconnectTimeout = useRef(null)
  const clientId = useRef(`client_${Date.now()}`)
  
  const connect = () => {
    try {
      ws.current = new WebSocket(`${WS_URL}${clientId.current}`)
      
      ws.current.onopen = () => {
        console.log('🌌 WebSocket Connected to ThaleOS')
        setIsConnected(true)
        
        // Clear any reconnect timeout
        if (reconnectTimeout.current) {
          clearTimeout(reconnectTimeout.current)
          reconnectTimeout.current = null
        }
      }
      
      ws.current.onmessage = (event) => {
        console.log('📨 Received message:', event.data)
        setLastMessage(event)
      }
      
      ws.current.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
      }
      
      ws.current.onclose = () => {
        console.log('🌑 WebSocket Disconnected')
        setIsConnected(false)
        
        // Attempt to reconnect after 3 seconds
        reconnectTimeout.current = setTimeout(() => {
          console.log('🔄 Attempting to reconnect...')
          connect()
        }, 3000)
      }
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
      setIsConnected(false)
    }
  }
  
  const disconnect = () => {
    if (ws.current) {
      ws.current.close()
    }
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current)
    }
  }
  
  const sendMessage = (message) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(message)
      console.log('📤 Sent message:', message)
    } else {
      console.error('WebSocket is not connected')
    }
  }
  
  useEffect(() => {
    return () => {
      disconnect()
    }
  }, [])
  
  return {
    isConnected,
    lastMessage,
    connect,
    disconnect,
    sendMessage,
  }
}
