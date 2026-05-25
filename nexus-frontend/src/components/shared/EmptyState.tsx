interface Props {
  icon?:    string
  title:    string
  message?: string
  action?:  { label: string; onClick: () => void }
}

export default function EmptyState({ icon = '◎', title, message, action }: Props) {
  return (
    <div style={{
      display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      padding: '48px 24px', gap: '12px',
      textAlign: 'center'
    }}>
      <div style={{
        fontSize: '28px', color: '#2d3748',
        fontFamily: 'JetBrains Mono, monospace',
        marginBottom: '4px'
      }}>{icon}</div>

      <p style={{
        fontSize: '13px', fontWeight: '600',
        fontFamily: 'JetBrains Mono, monospace',
        color: '#475569', margin: 0,
        letterSpacing: '0.06em'
      }}>{title}</p>

      {message && (
        <p style={{
          fontSize: '12px', color: '#334155',
          margin: 0, maxWidth: '280px', lineHeight: '1.6'
        }}>{message}</p>
      )}

      {action && (
        <button
          onClick={action.onClick}
          style={{
            marginTop: '8px',
            padding: '7px 18px',
            background: 'transparent',
            border: '1px solid #2d3748',
            borderRadius: '6px',
            color: '#94a3b8',
            fontSize: '11px',
            fontFamily: 'JetBrains Mono, monospace',
            cursor: 'pointer',
            letterSpacing: '0.06em',
            transition: 'border-color 0.2s, color 0.2s'
          }}
          onMouseEnter={e => {
            e.currentTarget.style.borderColor = '#00d4ff'
            e.currentTarget.style.color = '#00d4ff'
          }}
          onMouseLeave={e => {
            e.currentTarget.style.borderColor = '#2d3748'
            e.currentTarget.style.color = '#94a3b8'
          }}
        >{action.label}</button>
      )}
    </div>
  )
}
