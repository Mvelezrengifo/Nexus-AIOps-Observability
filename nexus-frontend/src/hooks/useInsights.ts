import { useEffect, useState } from 'react';

const mockInsights = [
  { id: '1', message: 'High latency detected in .NET service', confidence_score: 0.92, anomaly_type: 'latency', recommendation_level: 'high', timestamp: new Date().toISOString() },
  { id: '2', message: 'Throughput spike in FastAPI', confidence_score: 0.78, anomaly_type: 'throughput', recommendation_level: 'medium', timestamp: new Date().toISOString() },
];

export const useInsights = () => {
  const [insights, setInsights] = useState(mockInsights);
  const [loading, setLoading] = useState(false);
  return { insights, loading };
};