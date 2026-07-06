import { Sidebar } from './Sidebar';

export function MainLayout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <main style={{ 
        flex: 1, 
        marginLeft: '260px', 
        padding: '32px 48px',
        maxWidth: '1200px'
      }}>
        <div style={{ animation: 'fadeIn 0.4s ease forwards' }}>
          {children}
        </div>
      </main>
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}
      </style>
    </div>
  );
}
