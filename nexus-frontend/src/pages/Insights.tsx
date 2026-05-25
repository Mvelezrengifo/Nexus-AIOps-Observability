import React from 'react';
import { ConfidenceChart } from '../components/charts/ConfidenceChart';
import { AnomalyChart } from '../components/charts/AnomalyChart';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';

const mockInsights = [
  {
    id: '1',
    message: 'High latency detected in .NET service',
    confidence_score: 0.92,
    anomaly_type: 'latency',
    recommendation_level: 'high',
    timestamp: new Date().toISOString(),
  },
  {
    id: '2',
    message: 'Throughput spike in FastAPI',
    confidence_score: 0.78,
    anomaly_type: 'throughput',
    recommendation_level: 'medium',
    timestamp: new Date().toISOString(),
  },
];

export const Insights = () => {
  const insights = mockInsights;
  const loading = false;

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">AI Insights</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <ConfidenceChart data={insights} />
        <AnomalyChart data={insights} />
      </div>
      <div className="space-y-4">
        {insights.map((insight) => (
          <div key={insight.id} className="bg-gray-900 rounded-xl border border-gray-700 p-4">
            <p className="text-gray-200">{insight.message}</p>
            <div className="flex gap-4 mt-2 text-sm text-gray-400">
              <span>Confidence: {(insight.confidence_score * 100).toFixed(0)}%</span>
              <span>Type: {insight.anomaly_type}</span>
              <span>Recommendation: {insight.recommendation_level}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Insights;