import nexusApi from './nexusApi'
import type { ScoringRequest, ScoringResult } from '../types/insights'

export const scoringService = {
  score: async (payload: ScoringRequest): Promise<ScoringResult> => {
    const { data } = await nexusApi.post<ScoringResult>('/scoring', payload)
    return data
  }
}
