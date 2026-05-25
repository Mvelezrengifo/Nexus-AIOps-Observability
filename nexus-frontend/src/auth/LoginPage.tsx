import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthProvider';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard', { replace: true });
    } catch {
      setError('Invalid credentials. Access denied.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: '#080c14',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: 'IBM Plex Sans, sans-serif',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Grid background */}
      <div style={{
        position: 'absolute', inset: 0,
        backgroundImage: `
          linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px)
        `,
        backgroundSize: '40px 40px'
      }} />

      <div style={{
        position: 'relative',
        width: '100%', maxWidth: '420px',
        padding: '48px 40px',
        background: '#0d1117',
        border: '1px solid #1e293b',
        borderRadius: '12px',
        boxShadow: '0 0 0 1px #1e293b, 0 0 40px rgba(0,212,255,0.08)',
      }}>
        {/* Logo area con imagen oficial */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: '10px',
            marginBottom: '8px'
          }}>
            <img src="/nexus-logo.svg" alt="Nexus Logo" style={{ height: '32px', width: 'auto' }} />
            <span style={{
              fontFamily: 'JetBrains Mono, monospace',
              fontSize: '22px', fontWeight: '700',
              color: '#e2e8f0', letterSpacing: '0.1em'
            }}>NEXUS</span>
          </div>
          <p style={{ color: '#475569', fontSize: '12px', fontFamily: 'JetBrains Mono, monospace' }}>
            OPERATIONAL INTELLIGENCE PLATFORM
          </p>
        </div>

        {/* Formulario (igual que antes) */}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{
              display: 'block', marginBottom: '6px',
              fontSize: '11px', fontWeight: '600',
              color: '#94a3b8', letterSpacing: '0.08em',
              fontFamily: 'JetBrains Mono, monospace'
            }}>EMAIL</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              placeholder="operator@nexus.io"
              style={{
                width: '100%', padding: '12px 14px',
                background: '#111827',
                border: '1px solid #2d3748',
                borderRadius: '8px',
                color: '#e2e8f0', fontSize: '14px',
                outline: 'none', boxSizing: 'border-box',
                fontFamily: 'IBM Plex Sans, sans-serif',
                transition: 'border-color 0.2s'
              }}
              onFocus={e => e.target.style.borderColor = '#00d4ff'}
              onBlur={e => e.target.style.borderColor = '#2d3748'}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{
              display: 'block', marginBottom: '6px',
              fontSize: '11px', fontWeight: '600',
              color: '#94a3b8', letterSpacing: '0.08em',
              fontFamily: 'JetBrains Mono, monospace'
            }}>PASSWORD</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              placeholder="••••••••••••"
              style={{
                width: '100%', padding: '12px 14px',
                background: '#111827',
                border: '1px solid #2d3748',
                borderRadius: '8px',
                color: '#e2e8f0', fontSize: '14px',
                outline: 'none', boxSizing: 'border-box',
                fontFamily: 'IBM Plex Sans, sans-serif',
                transition: 'border-color 0.2s'
              }}
              onFocus={e => e.target.style.borderColor = '#00d4ff'}
              onBlur={e => e.target.style.borderColor = '#2d3748'}
            />
          </div>

          {error && (
            <div style={{
              padding: '10px 14px', marginBottom: '16px',
              background: 'rgba(255,61,90,0.1)',
              border: '1px solid rgba(255,61,90,0.3)',
              borderRadius: '8px',
              color: '#ff3d5a', fontSize: '13px'
            }}>{error}</div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%', padding: '13px',
              background: loading ? '#00a8cc' : '#00d4ff',
              border: 'none', borderRadius: '8px',
              color: '#080c14', fontSize: '13px',
              fontWeight: '700', letterSpacing: '0.08em',
              fontFamily: 'JetBrains Mono, monospace',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'background 0.2s'
            }}
          >
            {loading ? 'AUTHENTICATING...' : 'ACCESS NEXUS'}
          </button>
        </form>

        <p style={{
          textAlign: 'center', marginTop: '24px',
          fontSize: '11px', color: '#475569',
          fontFamily: 'JetBrains Mono, monospace'
        }}>
          NEXUS v1.0 · MokesoftIA · Authorized access only
        </p>
      </div>
    </div>
  );
}