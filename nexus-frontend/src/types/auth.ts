export interface User {
  id:       string
  email:    string
  name:     string
  role:     'admin' | 'operator' | 'viewer'
}

export interface AuthState {
  user:       User | null
  token:      string | null
  isAuth:     boolean
}

export interface LoginCredentials {
  email:    string
  password: string
}

export interface AuthResponse {
  user:         User
  access_token: string
  token_type:   string
}
