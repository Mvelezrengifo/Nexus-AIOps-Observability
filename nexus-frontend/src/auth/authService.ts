import nexusApi from '../api/nexusApi'
import type { AuthResponse, LoginCredentials } from '../types/auth'

export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const { data } = await nexusApi.post<AuthResponse>('/auth/login', credentials)
    return data
  },

  logout: async (): Promise<void> => {
    await nexusApi.post('/auth/logout').catch(() => {})
  },

  me: async () => {
    const { data } = await nexusApi.get('/auth/me')
    return data
  }
}
