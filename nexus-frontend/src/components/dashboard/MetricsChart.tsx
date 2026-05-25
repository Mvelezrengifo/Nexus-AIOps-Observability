import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export const MetricsChart = ({ metricType, title, data = [] }: { metricType: string; title: string; data?: any[] }) => {
  const chartData = data.length ? data : [{ timestamp: 'No data', value: 0 }];

  return (
    <div className="bg-gray-900 p-4 rounded-xl border border-gray-700">
      <h3 className="text-white text-lg font-semibold mb-2">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="timestamp" stroke="#9CA3AF" />
          <YAxis stroke="#9CA3AF" />
          <Tooltip
            contentStyle={{ backgroundColor: '#1F2937', borderColor: '#4B5563' }}
            labelStyle={{ color: '#F9FAFB' }}
          />
          <Line type="monotone" dataKey="value" stroke="#60A5FA" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};