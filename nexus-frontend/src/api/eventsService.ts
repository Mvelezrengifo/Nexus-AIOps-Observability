import nexusApi from './nexusApi'
import type { OperationalEvent, EventRequest } from '../types/events'

export const eventsService = {
  getAll: async (limit = 50): Promise<OperationalEvent[]> => {
    const { data } = await nexusApi.get<OperationalEvent[]>('/events', {
      params: { limit }
    })
    return data
  },

  create: async (payload: EventRequest): Promise<OperationalEvent> => {
    const { data } = await nexusApi.post<OperationalEvent>('/events', payload)
    return data
  }
}
