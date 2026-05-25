import { useEffect } from 'react'
import { nexusSocket } from './nexusSocket'
import { useNexusStore, selectEvents, selectLiveActive } from '../store/nexusStore'
import type { OperationalEvent } from '../types/events'

export function useEventStream() {
  const events     = useNexusStore(selectEvents)
  const liveActive = useNexusStore(selectLiveActive)

  useEffect(() => {
    nexusSocket.connect()

    // Handler specifically for this hook if extra logic needed
    const handler = (_event: OperationalEvent) => {
      // Store already updated via nexusSocket._handleGlobal
      // Add hook-specific logic here if needed
    }

    nexusSocket.on('event.new', handler as (data: unknown) => void)

    return () => {
      nexusSocket.off('event.new', handler as (data: unknown) => void)
    }
  }, [])

  return { events, liveActive }
}
