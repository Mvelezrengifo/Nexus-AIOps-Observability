import { useEffect } from 'react';
import { useNexusStore } from '../store/nexusStore';

export const useMockData = () => {
  const pushMetric = useNexusStore((state) => state.pushMetric);
  const addEvent = useNexusStore((state) => state.addEvent);

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date().toLocaleTimeString();

      // 1. Simular Métricas (Latencia, CPU, etc.)
      pushMetric('latency', { timestamp: now, value: Math.floor(Math.random() * 40) + 10 });
      pushMetric('cpuUsage', { timestamp: now, value: Math.floor(Math.random() * 30) + 20 });
      pushMetric('throughput', { timestamp: now, value: Math.floor(Math.random() * 1000) + 500 });
      pushMetric('confidence', { timestamp: now, value: Math.floor(Math.random() * 15) + 85 });
      pushMetric('scoring', { timestamp: now, value: Math.floor(Math.random() * 10) + 90 });

      // 2. Simular Anomalías (Ocasionales para que se vea real)
      if (Math.random() > 0.8) {
        pushMetric('anomalies', { timestamp: now, value: Math.floor(Math.random() * 100) });
      }

      // 3. Simular Eventos en el log
      if (Math.random() > 0.7) {
        const events = [
          "PostgreSQL: Slow query detected in 'users' table",
          "Service: Auth degradation in US-EAST-1",
          "AI: High confidence prediction for cluster B",
          "System: Memory spike handled by Autoscaler"
        ];
        addEvent({
          id: Date.now(),
          timestamp: now,
          message: events[Math.floor(Math.random() * events.length)],
          type: Math.random() > 0.8 ? 'warning' : 'info'
        });
      }
    }, 3000); // Actualiza cada 3 segundos

    return () => clearInterval(interval);
  }, [pushMetric, addEvent]);
};