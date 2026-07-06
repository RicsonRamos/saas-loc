
interface CardProps {
  children: React.ReactNode;
  title?: string;
  className?: string;
}

export function Card({ children, title, className = '' }: CardProps) {
  return (
    <div className={`glass-card p-6 ${className}`} style={{ padding: '24px' }}>
      {title && (
        <h3 style={{
          marginBottom: '16px',
          fontSize: '1.25rem',
          fontWeight: 600,
          color: 'var(--text-main)',
          borderBottom: '1px solid var(--border-color)',
          paddingBottom: '12px'
        }}>
          {title}
        </h3>
      )}
      <div>{children}</div>
    </div>
  );
}
