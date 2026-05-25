import { useEffect, useState } from 'react';

const mockEvents = [
  { id: '1', title: 'High CPU usage', severity: 'high', timestamp: new Date().toISOString(), message: 'CPU above 90%' },
  { id: '2', title: 'Memory leak detected', severity: 'critical', timestamp: new Date().toISOString(), message: 'Memory usage increasing' },
  { id: '3', title: 'Service degraded', severity: 'medium', timestamp: new Date().toISOString(), message: '.NET service responding slowly' },
];

export const useEvents = () => {
  const [events, setEvents] = useState(mockEvents);
  const [loading, setLoading] = useState(false);
  return { events, loading };
};