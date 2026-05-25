import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useMetricsStore } from '../../store/nexusStore';

export const ScoringChart = () => {
  const scoringHistory = useMetricsStore((state) => state.scoringHistory) || [];
  // 🛡️ Ajustamos para que lea 'value' que es lo que manda el mock
  const data = scoringHistory.length > 0 ? scoringHistory : [{ timestamp: '', value: 0 }];

  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <XAxis dataKey="timestamp" hide />
        <YAxis stroke="#475569" fontSize={10} domain={[0, 100]} tickLine={false} axisLine={false} />
        <Tooltip
           contentStyle={{ backgroundColor: '#0f172a', border: 'none', borderRadius: '8px' }}
        />
        <Line type="monotone" dataKey="value" stroke="#10B981" strokeWidth={3} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
};