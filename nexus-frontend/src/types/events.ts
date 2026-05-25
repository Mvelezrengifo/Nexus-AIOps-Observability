export type EventSeverity = 'info' | 'warning' | 'critical'
export type EventStatus   = 'open' | 'resolved' | 'investigating'

export interface OperationalEvent {
  id:           string
  service:      string
  severity:     EventSeverity
  status:       EventStatus
  message:      string
  timestamp:    string
  source_ip?:   string
  metadata?:    Record<string, unknown>
}

export interface EventRequest {
  service:   string
  severity:  EventSeverity
  message:   string
  metadata?: Record<string, unknown>
}
