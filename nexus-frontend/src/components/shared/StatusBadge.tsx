export const StatusBadge = ({ status }: { status: 'healthy' | 'degraded' | 'down' | 'warning' | 'ok' }) => {
  const colors = {
    healthy: 'bg-green-500/20 text-green-400 border-green-500/30',
    ok: 'bg-green-500/20 text-green-400 border-green-500/30',
    degraded: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    warning: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    down: 'bg-red-500/20 text-red-400 border-red-500/30',
  };
  return (
    <span className={`px-2 py-1 rounded-full text-xs font-mono border ${colors[status] || colors.degraded}`}>
      {status.toUpperCase()}
    </span>
  );
};