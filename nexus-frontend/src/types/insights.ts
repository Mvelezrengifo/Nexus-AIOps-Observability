export type AnomalyType       = 'latency' | 'error_rate' | 'throughput' | 'memory' | 'custom'
export type RecommendationLevel = 'low' | 'medium' | 'high' | 'critical'

export interface Insight {
  id:                   string
  confidence_score:     number        // 0.0 - 1.0
  anomaly_type:         AnomalyType
  source_service:       string
  recommendation_level: RecommendationLevel
  summary:              string
  recommendation:       string
  timestamp:            string
  metadata?:            Record<string, unknown>
}

export interface InsightRequest {
  service:  string
  context:  string
  metrics?: Record<string, number>
}

export interface ScoringRequest {
  service:  string
  metrics:  Record<string, number>
}

export interface ScoringResult {
  service:       string
  score:         number
  level:         RecommendationLevel
  breakdown:     Record<string, number>
  timestamp:     string
}

export interface PredictRequest {
  service:   string
  window_h:  number
  metrics:   Record<string, number[]>
}

export interface PredictResult {
  service:    string
  prediction: Record<string, number>
  confidence: number
  horizon_h:  number
  timestamp:  string
}
