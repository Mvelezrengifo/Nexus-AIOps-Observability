import React from 'react';
import { useInsights } from '../../hooks/useInsights';
import { SkeletonLoader } from '../shared/SkeletonLoader';

export const AIInsightsPanel: React.FC = () => {
  const { insights, loading } = useInsights();

  if (loading) return <SkeletonLoader width="100%" height="150px" />;

  return (
    <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
      <h3 className="text-white text-lg font-semibold mb-3">AI Insights</h3>
      <div className="space-y-3">
        {insights.map((insight) => (
          <div key={insight.id} className="border-l-4 border-blue-500 pl-3">
            <p className="text-gray-200 text-sm">{insight.message}</p>
            <div className="flex gap-2 mt-1 text-xs text-gray-400">
              <span>Confidence: {(insight.confidence_score * 100).toFixed(0)}%</span>
              <span>Type: {insight.anomaly_type}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};