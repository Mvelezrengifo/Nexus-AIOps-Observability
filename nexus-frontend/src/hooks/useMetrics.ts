import { useState } from 'react';

export const useMetrics = (type: string) => {
  const [data, setData] = useState([
    { timestamp: '10:00', value: 100 },
    { timestamp: '10:05', value: 120 },
    { timestamp: '10:10', value: 115 },
  ]);
  return data;
};