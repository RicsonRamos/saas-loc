import { InputHTMLAttributes, forwardRef } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = '', ...props }, ref) => {
    return (
      <div style={{ marginBottom: '16px', width: '100%' }} className={className}>
        {label && (
          <label style={{
            display: 'block',
            marginBottom: '6px',
            color: 'var(--text-muted)',
            fontSize: '0.875rem',
            fontWeight: 500
          }}>
            {label}
          </label>
        )}
        <input
          ref={ref}
          style={{
            width: '100%',
            padding: '10px 14px',
            borderRadius: 'var(--radius-sm)',
            border: `1px solid ${error ? 'var(--error)' : 'var(--border-color)'}`,
            background: 'rgba(15, 23, 42, 0.4)',
            color: 'var(--text-main)',
            fontSize: '0.95rem',
            outline: 'none',
            transition: 'all 0.2s ease',
          }}
          {...props}
        />
        {error && (
          <span style={{
            display: 'block',
            marginTop: '6px',
            color: 'var(--error)',
            fontSize: '0.8rem'
          }}>
            {error}
          </span>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';
