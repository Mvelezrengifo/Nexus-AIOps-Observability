interface AlertEvent {
  id: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  timestamp: string;
  message?: string;
}

export const AlertCard = ({ event }: { event: AlertEvent }) => {
  const severityColors = {
    critical: 'border-red-500 bg-red-500/10',
    high: 'border-orange-500 bg-orange-500/10',
    medium: 'border-yellow-500 bg-yellow-500/10',
    low: 'border-blue-500 bg-blue-500/10',
  };
  return (
    <div className={`border-l-4 p-3 rounded-r-lg ${severityColors[event.severity]} bg-gray-800`}>
      <div className="flex justify-between">
        <span className="font-bold text-white">{event.title}</span>
        <span className="text-xs text-gray-400">{new Date(event.timestamp).toLocaleTimeString()}</span>
      </div>
      {event.message && <p className="text-sm text-gray-300 mt-1">{event.message}</p>}
    </div>
  );
};