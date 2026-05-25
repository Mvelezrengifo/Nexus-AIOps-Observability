export type ServiceStatus = 'healthy' | 'warning' | 'critical' | 'unknown'

export interface ServiceHealth {
  name:        string
  status:      ServiceStatus
  latency_ms:  number
  last_check:  string
  message?:    string
}

export interface HealthStatus {
  status:    ServiceStatus
  timestamp: string
  version:   string
  services:  ServiceHealth[]
  uptime_s:  number
}
