import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useMetricsStore } from '../../store/nexusStore';

export const ConfidenceChart = () => {
  const confidenceHistory = useMetricsStore((state) => state.confidenceHistory) || [];

  // 🛡️ Mapeamos para que la gráfica entienda que 'value' es lo que queremos mostrar
  const chartData = confidenceHistory.length > 0
    ? confidenceHistory.map(item => ({
        name: item.timestamp,
        confidence: item.value
      }))
    : [{ name: '', confidence: 0 }];

  return (
    <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-800">
      <h4 className="text-gray-400 text-xs font-bold mb-4 uppercase tracking-wider">Confianza por Insight</h4>
      <ResponsiveContainer width="100%" height={150}>
        <BarChart data={chartData}>
          <XAxis dataKey="name" hide />
          <YAxis stroke="#475569" fontSize={10} domain={[0, 100]} tickLine={false} axisLine={false} />
          <Tooltip
            contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }}
          />
          <Bar dataKey="confidence" fill="#3B82F6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};