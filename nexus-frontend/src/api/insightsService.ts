import nexusApi from './nexusApi'
import type { Insight, InsightRequest } from '../types/insights'

export const insightsService = {
  getAll: async (): Promise<Insight[]> => {
    const { data } = await nexusApi.get<Insight[]>('/insights')
    return data
  },

  create: async (payload: InsightRequest): Promise<Insight> => {
    const { data } = await nexusApi.post<Insight>('/insights', payload)
    return data
  }
}
