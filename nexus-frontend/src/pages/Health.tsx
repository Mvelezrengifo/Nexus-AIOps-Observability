import React from 'react';
import { useHealth } from '../hooks/useHealth';
import { StatusBadge } from '../components/shared/StatusBadge';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';

export const Health: React.FC = () => {
  const { services, loading, error } = useHealth();

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-400">Error: {error}</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Service Health</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {services.map((svc) => (
          <div key={svc.name} className="bg-gray-900 rounded-xl border border-gray-700 p-4">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-white font-semibold">{svc.name}</h3>
                <p className="text-gray-400 text-sm">Latency: {svc.latency}ms</p>
              </div>
              <StatusBadge status={svc.status} />
            </div>
            {svc.message && (
              <p className="text-gray-500 text-sm mt-2">{svc.message}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Health;