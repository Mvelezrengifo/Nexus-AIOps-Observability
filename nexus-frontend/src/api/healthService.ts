import nexusApi from './nexusApi'
import type { HealthStatus } from '../types/health'

export const healthService = {
  getStatus: async (): Promise<HealthStatus> => {
    const { data } = await nexusApi.get<HealthStatus>('/health')
    return data
  }
}
