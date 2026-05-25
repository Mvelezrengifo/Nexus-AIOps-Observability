import React from 'react';
import { HealthMonitor } from '../components/dashboard/HealthMonitor';
import { EventStream } from '../components/dashboard/EventStream';
import { AIInsightsPanel } from '../components/dashboard/AIInsightsPanel';
import { ScoringWidget } from '../components/dashboard/ScoringWidget';
import { MetricsChart } from '../components/dashboard/MetricsChart';
import { ThroughputChart } from '../components/charts/ThroughputChart';
import { LatencyChart } from '../components/charts/LatencyChart';
import { ConfidenceChart } from '../components/charts/ConfidenceChart';
import { AnomalyChart } from '../components/charts/AnomalyChart';
import { ScoringChart } from '../components/charts/ScoringChart';

export const Dashboard = () => {
  return (
    <div className="p-6 bg-gray-950 min-h-screen">
      <h1 className="text-3xl font-bold text-white mb-6">Panel de control operativo</h1>

      {/* Grid principal: 3 columnas en pantallas grandes, 1 columna en móvil */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Primera columna */}
        <div className="space-y-6">
          <ScoringWidget />
          <div className="bg-gray-900 rounded-xl border border-gray-700 p-4">
            <h2 className="text-white text-xl font-bold mb-2">Puntuación operativa</h2>
            <ScoringChart />
          </div>
          <ThroughputChart />
        </div>

        {/* Segunda columna */}
        <div className="space-y-6">
          <HealthMonitor />
          <LatencyChart />
          <ConfidenceChart />
        </div>

        {/* Tercera columna */}
        <div className="space-y-6">
          <EventStream />
          <AnomalyChart />
        </div>

        {/* Fila completa para IA Insights */}
        <div className="lg:col-span-3">
          <AIInsightsPanel />
        </div>

        {/* Fila completa para métricas adicionales (si quieres mantener MetricsChart) */}
        <div className="lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-6">
          <MetricsChart metricType="throughput" title="Throughput" data={[]} />
          <MetricsChart metricType="latency" title="Latencia" data={[]} />
          <MetricsChart metricType="confidence" title="Confianza" data={[]} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;