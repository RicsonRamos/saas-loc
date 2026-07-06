import { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../services/supabaseClient';

export default function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      if (isLogin) {
        const { error: signInError } = await supabase.auth.signInWithPassword({
          email,
          password: senha,
        });

        if (signInError) throw signInError;
        
        // Supabase onAuthStateChange fará o redirect via contexto/app
        navigate('/');
      } else {
        const { error: signUpError } = await supabase.auth.signUp({
          email,
          password: senha,
        });

        if (signUpError) throw signUpError;
        
        setSuccess('Cadastro realizado! Verifique seu e-mail ou faça login (se e-mail confirmation estiver desabilitado).');
        setIsLogin(true);
      }
    } catch (err: any) {
      setError(err.message || 'Erro ao realizar autenticação');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'var(--bg-app)',
      backgroundImage: 'radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%), radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.15) 0px, transparent 50%)',
      fontFamily: "'Inter', sans-serif"
    }}>
      <div className="glass-panel" style={{
        width: '100%',
        maxWidth: '420px',
        padding: '40px',
        borderRadius: '16px',
        boxShadow: 'var(--shadow-glass)',
      }}>
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <h1 style={{
            fontSize: '2rem',
            fontFamily: "'Outfit', sans-serif",
            fontWeight: 700,
            color: 'var(--text-main)',
            marginBottom: '8px',
          }}>
            🚗 Locadora SaaS
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
            {isLogin ? 'Faça login para continuar' : 'Crie sua conta para começar'}
          </p>
        </div>

        <div style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
          <button
            type="button"
            onClick={() => setIsLogin(true)}
            style={{
              flex: 1,
              padding: '10px',
              border: 'none',
              background: isLogin ? 'var(--primary)' : 'rgba(255, 255, 255, 0.05)',
              color: isLogin ? '#fff' : 'var(--text-muted)',
              borderRadius: 'var(--radius-sm)',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            Login
          </button>
          <button
            type="button"
            onClick={() => setIsLogin(false)}
            style={{
              flex: 1,
              padding: '10px',
              border: 'none',
              background: !isLogin ? 'var(--primary)' : 'rgba(255, 255, 255, 0.05)',
              color: !isLogin ? '#fff' : 'var(--text-muted)',
              borderRadius: 'var(--radius-sm)',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            Cadastro
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              color: 'var(--text-main)',
              fontSize: '0.9rem',
              fontWeight: 500,
            }}>
              E-mail
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="seu@email.com"
              style={{
                width: '100%',
                padding: '12px 16px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-color)',
                background: 'rgba(15, 23, 42, 0.4)',
                color: 'var(--text-main)',
                fontSize: '1rem',
                outline: 'none',
                transition: 'border-color 0.3s ease',
              }}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{
              display: 'block',
              marginBottom: '8px',
              color: 'var(--text-main)',
              fontSize: '0.9rem',
              fontWeight: 500,
            }}>
              Senha
            </label>
            <input
              type="password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
              minLength={6}
              placeholder="Mínimo 6 caracteres"
              style={{
                width: '100%',
                padding: '12px 16px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-color)',
                background: 'rgba(15, 23, 42, 0.4)',
                color: 'var(--text-main)',
                fontSize: '1rem',
                outline: 'none',
                transition: 'border-color 0.3s ease',
              }}
            />
          </div>

          {error && (
            <div style={{
              padding: '12px',
              borderRadius: 'var(--radius-sm)',
              background: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              color: 'var(--error)',
              fontSize: '0.9rem',
              marginBottom: '20px',
              textAlign: 'center',
            }}>
              {error}
            </div>
          )}

          {success && (
            <div style={{
              padding: '12px',
              borderRadius: 'var(--radius-sm)',
              background: 'rgba(16, 185, 129, 0.15)',
              border: '1px solid rgba(16, 185, 129, 0.3)',
              color: 'var(--success)',
              fontSize: '0.9rem',
              marginBottom: '20px',
              textAlign: 'center',
            }}>
              {success}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '14px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              background: 'var(--primary)',
              color: '#fff',
              fontSize: '1rem',
              fontWeight: 600,
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1,
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 15px rgba(99, 102, 241, 0.4)',
            }}
          >
            {loading ? 'Aguarde...' : (isLogin ? 'Entrar' : 'Cadastrar')}
          </button>
        </form>
      </div>
    </div>
  );
}
