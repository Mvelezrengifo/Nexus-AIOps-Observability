// src/api/mockService.ts
export function generateMockEvent() {
  const events = [
    {
      type: "CPU High",
      value: `${Math.floor(Math.random() * 20) + 80}%`, // 80–100%
      message: "Uso de CPU por encima del 90%",
      confidence: 0.92,
      recommendation: "Escalar servicio o revisar procesos"
    },
    {
      type: "Memory Spike",
      value: `${Math.floor(Math.random() * 500) + 200} MB`,
      message: "Fuga de memoria detectada",
      confidence: 0.81,
      recommendation: "Optimizar manejo de memoria"
    },
    {
      type: "Latency",
      value: `${Math.floor(Math.random() * 200) + 100} ms`,
      message: "Alta latencia en GraphQL",
      confidence: 0.87,
      recommendation: "Revisar dependencias y balanceo"
    },
    {
      type: "Queue Backlog",
      value: `${Math.floor(Math.random() * 300) + 50}`,
      message: "Backlog en SQS",
      confidence: 0.76,
      recommendation: "Procesar mensajes pendientes"
    },
    {
      type: "Service Degraded",
      value: "Degradado",
      message: ".NET responde lentamente",
      confidence: 0.89,
      recommendation: "Escalar instancia o revisar logs"
    }
  ];
  return events[Math.floor(Math.random() * events.length)];
}

export function startMockStream(callback: (event: any) => void) {
  setInterval(() => {
    const event = generateMockEvent();
    callback(event);
  }, 5000);
}
