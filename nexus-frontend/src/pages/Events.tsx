import React from 'react';
import { useEvents } from '../hooks/useEvents';
import { AlertCard } from '../components/shared/AlertCard';
import { LoadingSpinner } from '../components/shared/LoadingSpinner';

export const Events: React.FC = () => {
  const { events, loading } = useEvents();

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Event Stream</h1>
      <div className="space-y-3">
        {events.map((event) => (
          <AlertCard key={event.id} event={event} />
        ))}
      </div>
    </div>
  );
};

export default Events;