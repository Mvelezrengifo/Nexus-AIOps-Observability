import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { createAuthSlice,    type AuthSlice    } from './authSlice'
import { createEventsSlice,  type EventsSlice  } from './eventsSlice'
import { createAlertsSlice,  type AlertsSlice  } from './alertsSlice'
import { createMetricsSlice, type MetricsSlice } from './metricsSlice'

// Combined store type
export type NexusStore = AuthSlice & EventsSlice & AlertsSlice & MetricsSlice

export const useNexusStore = create<NexusStore>()(
  devtools(
    (...a) => ({
      ...createAuthSlice(...a),
      ...createEventsSlice(...a),
      ...createAlertsSlice(...a),
      ...createMetricsSlice(...a),
    }),
    { name: 'NexusStore' }
  )
)

// --- SELECTORES (Los cables que conectan con los componentes) ---
export const selectUser       = (s: NexusStore) => s.user
export const selectIsAuth     = (s: NexusStore) => s.isAuth
export const selectEvents     = (s: NexusStore) => s.events || []
export const selectLiveActive = (s: NexusStore) => s.isLive // Ajustado a isLive de tus capturas
export const selectAlerts     = (s: NexusStore) => s.alerts || []
export const selectUnread     = (s: NexusStore) => (s.alerts || []).length

// Selectores para los Gráficos (Aseguramos que siempre devuelvan un array para evitar errores de .reduce)
export const selectLatency    = (s: NexusStore) => s.latencyHistory || []
export const selectThroughput = (s: NexusStore) => s.throughputHistory || []
export const selectScoring    = (s: NexusStore) => s.scoringHistory || []
export const selectConfidence = (s: NexusStore) => s.confidenceHistory || []
export const selectCpuUsage   = (s: NexusStore) => s.cpuUsageHistory || []
export const selectErrorRate  = (s: NexusStore) => s.errorRateHistory || []
export const selectAnomalies  = (s: NexusStore) => s.anomalies || []

// 🛡️ ALIAS MAESTRO: Para que los componentes viejos sigan funcionando sin cambiar sus imports
export const useMetricsStore = useNexusStore;