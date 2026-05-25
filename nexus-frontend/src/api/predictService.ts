import nexusApi from './nexusApi'
import type { PredictRequest, PredictResult } from '../types/insights'

export const predictService = {
  predict: async (payload: PredictRequest): Promise<PredictResult> => {
    const { data } = await nexusApi.post<PredictResult>('/predict', payload)
    return data
  }
}
