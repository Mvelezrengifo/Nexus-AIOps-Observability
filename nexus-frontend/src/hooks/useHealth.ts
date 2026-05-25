// src/hooks/useHealth.ts
import { useEffect, useState } from 'react';

// Datos mock para que funcione ya
const mockServices = [
  { name: 'GraphQL Gateway', status: 'healthy', latency: 45 },
  { name: 'FastAPI (AI)', status: 'healthy', latency: 78 },
  { name: '.NET Enterprise', status: 'degraded', latency: 210 },
  { name: 'PostgreSQL', status: 'healthy', latency: 12 },
];

export const useHealth = () => {
  const [services, setServices] = useState(mockServices);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Aquí después conectas con el backend real
  return { services, loading, error };
};