import type { User } from '../types/auth'

export interface AuthSlice {
  user:       User | null
  isAuth:     boolean
  setUser:    (user: User | null) => void
  clearAuth:  () => void
}

export const createAuthSlice = (set: (fn: (state: AuthSlice) => Partial<AuthSlice>) => void): AuthSlice => ({
  user:    null,
  isAuth:  false,

  setUser: (user) => set(() => ({
    user,
    isAuth: !!user
  })),

  clearAuth: () => set(() => ({
    user:   null,
    isAuth: false
  }))
})
