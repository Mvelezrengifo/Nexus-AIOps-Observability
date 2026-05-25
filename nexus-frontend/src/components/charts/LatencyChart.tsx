import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useNexusStore } from '../../store/nexusStore';

export const LatencyChart = () => {
  const latencyHistory = useNexusStore((state) => state.latencyHistory);
  const data = latencyHistory.length ? latencyHistory : [{ timestamp: 'No data', value: 0 }];

  return (
    <div className="bg-gray-800 p-3 rounded-lg">
      <h4 className="text-gray-300 text-sm mb-2">Latency (ms)</h4>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data}>
          <XAxis dataKey="timestamp" stroke="#6B7280" fontSize={10} />
          <YAxis stroke="#6B7280" fontSize={10} />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#F59E0B" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
