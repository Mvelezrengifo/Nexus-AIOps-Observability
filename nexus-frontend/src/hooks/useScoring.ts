import { useState } from 'react';

export const useScoring = () => {
  const [score, setScore] = useState(87);
  const [trend, setTrend] = useState(5);
  const [history, setHistory] = useState([
    { timestamp: '10:00', score: 82 },
    { timestamp: '10:05', score: 84 },
    { timestamp: '10:10', score: 87 },
  ]);
  return { score, trend, history };
};