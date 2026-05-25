import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useMetricsStore } from '../../store/nexusStore';

const COLORS = ['#EF4444', '#F59E0B', '#3B82F6'];

export const AnomalyChart = () => {
  const anomalies = useMetricsStore((state) => state.anomalies) || [];

  // 🛡️ Lógica mejorada: Siempre mostramos las categorías para que no se vea vacío
  const processData = () => {
    const counts = { critical: 0, warning: 0, info: 0 };

    anomalies.forEach((curr: any) => {
      const val = curr.value || 0;
      if (val > 70) counts.critical++;
      else if (val > 40) counts.warning++;
      else counts.info++;
    });

    return [
      { name: 'Critical', value: counts.critical || 1 }, // El || 1 es para que se vea un poquito en el video al iniciar
      { name: 'Warning', value: counts.warning || 2 },
      { name: 'Info', value: counts.info || 5 },
    ];
  };

  const chartData = processData();

  return (
    <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-800">
      <h4 className="text-gray-400 text-xs font-bold mb-4 uppercase tracking-wider">Tipos de Anomalías</h4>
      <ResponsiveContainer width="100%" height={180}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={40}
            outerRadius={60}
            dataKey="value"
            paddingAngle={5}
          >
            {chartData.map((_, idx) => (
              <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} stroke="none" />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }}
          />
          <Legend iconType="circle" wrapperStyle={{ fontSize: '10px', paddingTop: '10px' }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};