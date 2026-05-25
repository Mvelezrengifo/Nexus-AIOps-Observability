import { useEffect, useState } from 'react'
import { nexusSocket } from './nexusSocket'
import { healthService } from '../api/healthService'
import type { HealthStatus } from '../types/health'

export function useHealthStream() {
  const [health,  setHealth]  = useState<HealthStatus | null>(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState<string | null>(null)

  useEffect(() => {
    // Initial fetch
    healthService.getStatus()
      .then(setHealth)
      .catch(() => setError('Failed to fetch health status'))
      .finally(() => setLoading(false))

    // Live updates via WebSocket
    const handler = (data: unknown) => {
      setHealth(data as HealthStatus)
      setError(null)
    }

    nexusSocket.connect()
    nexusSocket.on('health.update', handler)

    return () => {
      nexusSocket.off('health.update', handler)
    }
  }, [])

  return { health, loading, error }
}
