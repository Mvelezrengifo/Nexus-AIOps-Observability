import { Component, type ReactNode, type ErrorInfo } from 'react'

interface Props {
  children:  ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error:    Error | null
}

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('[NEXUS ErrorBoundary]', error, info)
  }

  reset = () => this.setState({ hasError: false, error: null })

  render() {
    if (!this.state.hasError) return this.props.children

    if (this.props.fallback) return this.props.fallback

    return (
      <div style={{
        display: 'flex', flexDirection: 'column',
        alignItems: 'center', justifyContent: 'center',
        padding: '40px 24px', gap: '16px',
        background: '#0d1117',
        border: '1px solid rgba(255,61,90,0.3)',
        borderRadius: '12px',
        textAlign: 'center'
      }}>
        <div style={{
          width: '48px', height: '48px',
          borderRadius: '50%',
          background: 'rgba(255,61,90,0.1)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '22px'
        }}>⚠</div>

        <div>
          <p style={{
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: '13px', fontWeight: '600',
            color: '#ff3d5a', marginBottom: '6px'
          }}>MODULE RENDER ERROR</p>
          <p style={{
            fontSize: '12px', color: '#475569',
            fontFamily: 'JetBrains Mono, monospace',
            maxWidth: '320px'
          }}>
            {this.state.error?.message || 'An unexpected error occurred'}
          </p>
        </div>

        <button
          onClick={this.reset}
          style={{
            padding: '8px 20px',
            background: 'transparent',
            border: '1px solid #ff3d5a',
            borderRadius: '6px',
            color: '#ff3d5a',
            fontSize: '11px',
            fontFamily: 'JetBrains Mono, monospace',
            cursor: 'pointer',
            letterSpacing: '0.08em'
          }}
        >
          RETRY MODULE
        </button>
      </div>
    )
  }
}
