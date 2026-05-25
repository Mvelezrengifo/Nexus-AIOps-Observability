// src/api/metricsService.ts
export function generateMockMetrics() {
  return {
    timestamp: new Date().toISOString(),
    latencyAvg: Math.floor(Math.random() * 200) + 50,   // ms
    throughput: Math.floor(Math.random() * 500) + 100,  // eventos/segundo
    scoring: Math.floor(Math.random() * 20) + 80,       // 80–100
    anomalies: Math.floor(Math.random() * 5),           // cantidad
    confidence: (Math.random() * 0.2 + 0.8).toFixed(2)  // 0.80–1.00
  };
}

export function startMetricsStream(callback: (metrics: any) => void) {
  setInterval(() => {
    callback(generateMockMetrics());
  }, 4000);
}
