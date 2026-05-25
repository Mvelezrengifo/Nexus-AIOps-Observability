import { create } from 'zustand';
import { StateCreator } from 'zustand';

// Definimos la estructura completa para que nada falte
export interface MetricsSlice {
  latencyHistory: { timestamp: string; value: number }[];
  throughputHistory: { timestamp: string; value: number }[];
  scoringHistory: { timestamp: string; value: number }[];
  confidenceHistory: { timestamp: string; value: number }[];
  cpuUsageHistory: { timestamp: string; value: number }[];
  errorRateHistory: { timestamp: string; value: number }[];
  anomalies: any[];
  events: any[];
  alerts: any[];
  isLive: boolean;
  // Métodos que el Socket Manager necesita
  setLive: (status: boolean) => void;
  addEvent: (event: any) => void;
  addAlert: (alert: any) => void;
  pushMetric: (key: string, point: { timestamp: string; value: number }) => void;
}

export const createMetricsSlice: StateCreator<MetricsSlice> = (set) => ({
  latencyHistory: [],
  throughputHistory: [],
  scoringHistory: [],
  confidenceHistory: [],
  cpuUsageHistory: [],
  errorRateHistory: [],
  anomalies: [],
  events: [],
  alerts: [],
  isLive: false,

  setLive: (status) => set({ isLive: status }),

  addEvent: (event) => set((state) => ({
    events: [event, ...state.events].slice(0, 50)
  })),

  addAlert: (alert) => set((state) => ({
    alerts: [alert, ...state.alerts].slice(0, 20)
  })),

  pushMetric: (key, point) =>
    set((state) => {
      const historyKey = `${key}History` as keyof MetricsSlice;
      // Verificamos si existe el array, si no, lo creamos para evitar el error de 'reduce'
      const currentHistory = (state[historyKey] as any[]) || [];
      return {
        [historyKey]: [...currentHistory, point].slice(-50),
      };
    }),
});

// Creamos el store único
export const useMetricsStore = create<MetricsSlice>()((...a) => ({
  ...createMetricsSlice(...a),
}));

// Exportamos los alias para que Atlas y Seek encuentren lo que buscan
export const useNexusStore = useMetricsStore;