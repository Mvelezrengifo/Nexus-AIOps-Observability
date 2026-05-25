export type AlertLevel = 'info' | 'warning' | 'critical'

export interface Alert {
  id:        string
  level:     AlertLevel
  message:   string
  service?:  string
  timestamp: string
  read:      boolean
}

export interface AlertsSlice {
  alerts:      Alert[]
  unreadCount: number
  addAlert:    (alert: Omit<Alert, 'id' | 'read' | 'timestamp'>) => void
  markRead:    (id: string) => void
  markAllRead: () => void
  clearAlerts: () => void
}

export const createAlertsSlice = (set: (fn: (state: AlertsSlice) => Partial<AlertsSlice>) => void): AlertsSlice => ({
  alerts:      [],
  unreadCount: 0,

  addAlert: (alert) => set((state) => {
    const newAlert: Alert = {
      ...alert,
      id:        crypto.randomUUID(),
      read:      false,
      timestamp: new Date().toISOString()
    }
    const alerts = [newAlert, ...state.alerts].slice(0, 50)
    return {
      alerts,
      unreadCount: alerts.filter(a => !a.read).length
    }
  }),

  markRead: (id) => set((state) => {
    const alerts = state.alerts.map(a => a.id === id ? { ...a, read: true } : a)
    return { alerts, unreadCount: alerts.filter(a => !a.read).length }
  }),

  markAllRead: () => set((state) => ({
    alerts:      state.alerts.map(a => ({ ...a, read: true })),
    unreadCount: 0
  })),

  clearAlerts: () => set(() => ({ alerts: [], unreadCount: 0 }))
})
