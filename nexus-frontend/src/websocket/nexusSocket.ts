import { useNexusStore } from '../store/nexusStore'
import type { OperationalEvent } from '../types/events'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:5173'

type MessageHandler = (data: unknown) => void

class NexusSocketManager {
  private socket:    WebSocket | null = null
  private handlers:  Map<string, MessageHandler[]> = new Map()
  private reconnect: ReturnType<typeof setTimeout> | null = null
  private attempts:  number = 0
  private maxRetries = 5
  private mockInterval: ReturnType<typeof setInterval> | null = null

  connect() {
    if (this.socket?.readyState === WebSocket.OPEN) return

    const token = localStorage.getItem('nexus_token')
    const url   = token ? `${WS_URL}/ws?token=${token}` : `${WS_URL}/ws`

    try {
      this.socket = new WebSocket(url)
      this._bindEvents()
    } catch (err) {
      console.error('[NEXUS WS] Connection failed:', err)
      this._scheduleReconnect()
      this._startMockStream() // fallback simulado
    }
  }

  disconnect() {
    if (this.reconnect) clearTimeout(this.reconnect)
    if (this.mockInterval) clearInterval(this.mockInterval)
    this.socket?.close()
    this.socket   = null
    this.attempts = 0
  }

  on(event: string, handler: MessageHandler) {
    if (!this.handlers.has(event)) this.handlers.set(event, [])
    this.handlers.get(event)!.push(handler)
  }

  off(event: string, handler: MessageHandler) {
    const list = this.handlers.get(event) || []
    this.handlers.set(event, list.filter(h => h !== handler))
  }

  private _bindEvents() {
    if (!this.socket) return

    this.socket.onopen = () => {
      console.info('[NEXUS WS] Connected')
      this.attempts = 0
      useNexusStore.getState().setLive(true)
      if (this.mockInterval) clearInterval(this.mockInterval)
    }

    this.socket.onclose = () => {
      console.warn('[NEXUS WS] Disconnected')
      useNexusStore.getState().setLive(false)
      this._scheduleReconnect()
      this._startMockStream() // fallback simulado
    }

    this.socket.onerror = (err) => {
      console.error('[NEXUS WS] Error:', err)
    }

    this.socket.onmessage = (msg) => {
      try {
        const payload = JSON.parse(msg.data) as { type: string; data: unknown }
        this._dispatch(payload.type, payload.data)
        this._handleGlobal(payload.type, payload.data)
      } catch {
        console.warn('[NEXUS WS] Unparseable message:', msg.data)
      }
    }
  }

  private _dispatch(type: string, data: unknown) {
    const list = this.handlers.get(type) || []
    list.forEach(h => h(data))

    const wildcard = this.handlers.get('*') || []
    wildcard.forEach(h => h({ type, data }))
  }

  private _handleGlobal(type: string, data: unknown) {
    const store = useNexusStore.getState()

    switch (type) {
      case 'event.new':
        store.addEvent(data as OperationalEvent)
        if ((data as OperationalEvent).severity === 'critical') {
          store.addAlert({
            level:   'critical',
            message: (data as OperationalEvent).message,
            service: (data as OperationalEvent).service,
          })
        }
        break

      case 'metric.update':
        const m = data as { key: 'latency' | 'throughput' | 'errorRate' | 'cpuUsage'; point: { timestamp: string; value: number } }
        store.pushMetric(m.key, m.point)
        break

      case 'alert.new':
        store.addAlert(data as Parameters<typeof store.addAlert>[0])
        break
    }
  }

  private _scheduleReconnect() {
    if (this.attempts >= this.maxRetries) {
      console.error('[NEXUS WS] Max reconnect attempts reached')
      return
    }
    const delay = Math.min(1000 * 2 ** this.attempts, 30000)
    this.attempts++
    console.info(`[NEXUS WS] Reconnecting in ${delay}ms (attempt ${this.attempts})`)
    this.reconnect = setTimeout(() => this.connect(), delay)
  }

  // 🔹 Simulación de mensajes cuando no hay backend real
  private _startMockStream() {
    if (this.mockInterval) return
    console.info('[NEXUS WS] Starting mock stream...')
    this.mockInterval = setInterval(() => {
      const fakeEvent: OperationalEvent = {
        id: Date.now().toString(),
        service: 'FastAPI',
        message: 'Latencia simulada alta',
        severity: 'warning',
        timestamp: new Date().toISOString()
      }
      this._dispatch('event.new', fakeEvent)
      this._handleGlobal('event.new', fakeEvent)

      const fakeMetric = {
        key: 'latency',
        point: { timestamp: new Date().toISOString(), value: Math.floor(Math.random() * 200) + 50 }
      }
      this._dispatch('metric.update', fakeMetric)
      this._handleGlobal('metric.update', fakeMetric)
    }, 5000)
  }
}

// Singleton
export const nexusSocket = new NexusSocketManager()
