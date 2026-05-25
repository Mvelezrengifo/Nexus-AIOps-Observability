const TOKEN_KEY = 'nexus_token'

export const jwtHandler = {
  save: (token: string) => {
    localStorage.setItem(TOKEN_KEY, token)
  },

  get: (): string | null => {
    return localStorage.getItem(TOKEN_KEY)
  },

  remove: () => {
    localStorage.removeItem(TOKEN_KEY)
  },

  isValid: (): boolean => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (!token) return false
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.exp * 1000 > Date.now()
    } catch {
      return false
    }
  },

  decode: () => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (!token) return null
    try {
      return JSON.parse(atob(token.split('.')[1]))
    } catch {
      return null
    }
  }
}
