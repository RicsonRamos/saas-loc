import React from 'react';

type BadgeVariant = 'success' | 'warning' | 'error' | 'info' | 'default';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
}

export function Badge({ children, variant = 'default' }: BadgeProps) {
  let bgColor = 'rgba(255, 255, 255, 0.1)';
  let color = 'var(--text-main)';

  switch (variant) {
    case 'success':
      bgColor = 'rgba(16, 185, 129, 0.2)';
      color = '#34d399'; // Emerald 400
      break;
    case 'warning':
      bgColor = 'rgba(245, 158, 11, 0.2)';
      color = '#fbbf24'; // Amber 400
      break;
    case 'error':
      bgColor = 'rgba(239, 68, 68, 0.2)';
      color = '#f87171'; // Red 400
      break;
    case 'info':
      bgColor = 'rgba(99, 102, 241, 0.2)';
      color = '#818cf8'; // Indigo 400
      break;
  }

  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: '4px 8px',
      borderRadius: '9999px',
      fontSize: '0.75rem',
      fontWeight: 600,
      background: bgColor,
      color: color,
      border: `1px solid ${bgColor.replace('0.2)', '0.3)')}`
    }}>
      {children}
    </span>
  );
}
