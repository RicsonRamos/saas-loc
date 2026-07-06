import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  isLoading?: boolean;
}

export function Button({ 
  children, 
  variant = 'primary', 
  isLoading, 
  className = '', 
  disabled, 
  ...props 
}: ButtonProps) {
  
  const baseStyle = {
    padding: '10px 20px',
    borderRadius: 'var(--radius-sm)',
    border: 'none',
    fontSize: '0.95rem',
    fontWeight: 500,
    cursor: disabled || isLoading ? 'not-allowed' : 'pointer',
    opacity: disabled || isLoading ? 0.7 : 1,
    transition: 'all 0.2s ease',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px'
  };

  const variants = {
    primary: {
      background: 'var(--primary)',
      color: '#fff',
      boxShadow: '0 4px 10px rgba(99, 102, 241, 0.3)'
    },
    secondary: {
      background: 'rgba(255, 255, 255, 0.1)',
      color: 'var(--text-main)',
      border: '1px solid var(--border-color)'
    },
    danger: {
      background: 'rgba(239, 68, 68, 0.15)',
      color: 'var(--error)',
      border: '1px solid rgba(239, 68, 68, 0.3)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--text-muted)'
    }
  };

  return (
    <button 
      style={{ ...baseStyle, ...variants[variant] }} 
      className={className}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? 'Aguarde...' : children}
    </button>
  );
}
