import { NavLink } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

export function Sidebar() {
  const { logout } = useAuth();
  
  const menuItems = [
    { name: 'Dashboard', path: '/' },
    { name: 'Clientes', path: '/clientes' },
    { name: 'Frota', path: '/frota' },
    { name: 'Contratos', path: '/contratos' },
    { name: 'Financeiro', path: '/financeiro' },
  ];

  return (
    <aside style={{
      width: '260px',
      height: '100vh',
      position: 'fixed',
      left: 0,
      top: 0,
      background: 'var(--bg-sidebar)',
      backdropFilter: 'blur(12px)',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      padding: '24px 16px',
      zIndex: 50
    }}>
      <div style={{ padding: '0 12px 32px 12px' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#fff', margin: 0 }}>🚗 Locadora SaaS</h2>
        <span style={{ fontSize: '0.8rem', color: 'var(--primary-light)', fontWeight: 500 }}>Admin Panel</span>
      </div>
      
      <nav style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            style={({ isActive }) => ({
              padding: '12px 16px',
              borderRadius: 'var(--radius-md)',
              color: isActive ? '#fff' : 'var(--text-muted)',
              background: isActive ? 'var(--primary)' : 'transparent',
              fontWeight: isActive ? 600 : 500,
              transition: 'all 0.2s ease',
              display: 'flex',
              alignItems: 'center',
              boxShadow: isActive ? '0 4px 12px rgba(99, 102, 241, 0.4)' : 'none'
            })}
          >
            {item.name}
          </NavLink>
        ))}
      </nav>
      
      <div style={{ marginTop: 'auto', borderTop: '1px solid var(--border-color)', paddingTop: '24px' }}>
        <button
          onClick={logout}
          style={{
            width: '100%',
            padding: '12px',
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.2)',
            color: 'var(--error)',
            borderRadius: 'var(--radius-md)',
            fontWeight: 500,
            cursor: 'pointer',
            transition: 'all 0.2s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = 'rgba(239, 68, 68, 0.2)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)';
          }}
        >
          Sair do Sistema
        </button>
      </div>
    </aside>
  );
}
