import React from 'react';
import { useHealth } from '../../hooks/useHealth';
import { StatusBadge } from '../shared/StatusBadge';
import { LoadingSpinner } from '../shared/LoadingSpinner';

export const HealthMonitor = () => {
  const { services, loading, error } = useHealth();

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-400">Error: {error}</div>;

  return (
    <div className="bg-gray-900 rounded-xl border border-gray-700 p-4">
      <h2 className="text-white text-xl font-bold mb-4">Service Health</h2>
      <div className="space-y-2">
        {services.map((svc) => (
          <div key={svc.name} className="flex justify-between items-center">
            <span className="text-gray-300">{svc.name}</span>
            <StatusBadge status={svc.status as any} />
            <span className="text-gray-400 text-sm">{svc.latency}ms</span>
          </div>
        ))}
      </div>
    </div>
  );
};