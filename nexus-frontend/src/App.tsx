import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './auth/AuthProvider';
import ProtectedRoute from './auth/ProtectedRoute';
import LoginPage from './auth/LoginPage';
import Dashboard from './pages/Dashboard';
import Events from './pages/Events';
import Insights from './pages/Insights';
import Health from './pages/Health';
import MainLayout from './components/layout/MainLayout';
import { useNexusStore } from './store/nexusStore';

// --- MOTOR DE SIMULACIÓN (MOCK DATA) ---
// Este hook genera el movimiento profesional que necesitas para el video
const useMockDataGenerator = () => {
  const pushMetric = useNexusStore((state) => state.pushMetric);
  const addEvent = useNexusStore((state) => state.addEvent);

  useEffect(() => {
    // Generar datos iniciales para que no arranque vacío
    const categories = ['latency', 'cpuUsage', 'throughput', 'confidence', 'scoring'];
    categories.forEach(cat => {
      for(let i=0; i<10; i++) {
        pushMetric(cat, {
          timestamp: new Date(Date.now() - (10-i)*3000).toLocaleTimeString(),
          value: Math.floor(Math.random() * 20) + 70
        });
      }
    });

    const interval = setInterval(() => {
      const now = new Date().toLocaleTimeString();

      // Simulación de métricas dinámicas
      pushMetric('latency', { timestamp: now, value: Math.floor(Math.random() * 30) + 15 });
      pushMetric('cpuUsage', { timestamp: now, value: Math.floor(Math.random() * 25) + 40 });
      pushMetric('throughput', { timestamp: now, value: Math.floor(Math.random() * 100) + 800 });
      pushMetric('confidence', { timestamp: now, value: Math.floor(Math.random() * 10) + 88 });
      pushMetric('scoring', { timestamp: now, value: Math.floor(Math.random() * 5) + 94 });

      // Simulación de Anomalías (Aparecen de vez en cuando)
      if (Math.random() > 0.7) {
        pushMetric('anomalies', {
          timestamp: now,
          value: Math.floor(Math.random() * 100)
        });
      }

      // Log de eventos "Enterprise"
      if (Math.random() > 0.6) {
        const mockEvents = [
          { msg: "PostgreSQL: detectada consulta lenta (>200ms)", type: "warning" },
          { msg: "Redis: Cache hit rate optimizado al 98%", type: "info" },
          { msg: "Gateway: Intento de intrusión bloqueado (WAF)", type: "warning" },
          { msg: "Nexus AI: Nueva anomalía detectada en Cluster-B", type: "critical" },
          { msg: "System: Auto-scaling completado con éxito", type: "info" }
        ];
        const selected = mockEvents[Math.floor(Math.random() * mockEvents.length)];
        addEvent({
          id: Date.now(),
          timestamp: now,
          message: selected.msg,
          type: selected.type
        });
      }
    }, 3000); // Se mueve cada 3 segundos

    return () => clearInterval(interval);
  }, [pushMetric, addEvent]);
};

// --- COMPONENTE PRINCIPAL ---
export default function App() {
  // Activamos el generador de vida
  useMockDataGenerator();

  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedRoute />}>
            <Route element={<MainLayout />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/events" element={<Events />} />
              <Route path="/insights" element={<Insights />} />
              <Route path="/health" element={<Health />} />
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
            </Route>
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}