import React from 'react';
import { useNexusStore } from '../../store/nexusStore';
import { AlertCard } from '../shared/AlertCard';
import { SkeletonLoader } from '../shared/SkeletonLoader';

export const EventStream = () => {
  const events = useNexusStore((s) => s.events);

  if (!events) return <SkeletonLoader count={3} />;

  return (
    <div className="bg-gray-900 rounded-xl border border-gray-700 p-4">
      <h2 className="text-white text-xl font-bold mb-4">Real-time Events</h2>
      <div className="space-y-2 max-h-80 overflow-y-auto">
        {events.length === 0 && <div className="text-gray-500 text-center">No events yet</div>}
        {events.map((event) => (
          <AlertCard key={event.id} event={event} />
        ))}
      </div>
    </div>
  );
};
