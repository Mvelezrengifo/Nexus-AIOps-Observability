import React from 'react';
import { ScoringChart } from '../charts/ScoringChart';

const mockScore = 87;
const mockTrend = 5;
const mockHistory = [
  { timestamp: '10:00', score: 82 },
  { timestamp: '10:05', score: 84 },
  { timestamp: '10:10', score: 87 },
];

export const ScoringWidget: React.FC = () => {
  return (
    <div className="bg-gray-900 rounded-xl border border-gray-700 p-4">
      <h2 className="text-white text-xl font-bold mb-2">Operational Score</h2>
      <div className="text-4xl font-bold text-blue-400">{mockScore}</div>
      <div className={`text-sm ${mockTrend >= 0 ? 'text-green-400' : 'text-red-400'}`}>
        {mockTrend >= 0 ? '↑' : '↓'} {Math.abs(mockTrend)}% vs last hour
      </div>
      <div className="mt-4 h-32">
        <ScoringChart data={mockHistory} />
      </div>
    </div>
  );
};