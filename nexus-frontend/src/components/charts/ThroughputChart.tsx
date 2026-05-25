import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useMetricsStore } from '../../store/nexusStore'; // Usamos el store central

export const ThroughputChart = () => {
  const throughputHistory = useMetricsStore((state) => state.throughputHistory) || [];
  const data = throughputHistory.length > 0 ? throughputHistory : [{ timestamp: '', value: 0 }];

  return (
    <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-800">
      <h4 className="text-gray-400 text-xs font-bold mb-4 uppercase tracking-wider">Rendimiento (eventos/seg)</h4>
      <ResponsiveContainer width="100%" height={160}>
        <AreaChart data={data}>
          <XAxis dataKey="timestamp" hide />
          <YAxis stroke="#475569" fontSize={10} tickLine={false} axisLine={false} />
          <Tooltip
            contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }}
            itemStyle={{ color: '#8B5CF6' }}
          />
          <Area type="monotone" dataKey="value" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.1} strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};