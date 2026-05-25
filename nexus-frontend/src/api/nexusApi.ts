import axios from 'axios'

// Base URL apunta al backend FastAPI en puerto 5173
// En desarrollo el proxy de Vite redirige /api → localhost:5173
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5173'

export const nexusApi = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor: agrega JWT automáticamente
nexusApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('nexus_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor: manejo global de errores
nexusApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('nexus_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default nexusApi
