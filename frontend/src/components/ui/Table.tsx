
interface Column<T> {
  header: string;
  accessor: keyof T | ((row: T) => React.ReactNode);
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (item: T) => string | number;
  emptyMessage?: string;
}

export function Table<T>({ columns, data, keyExtractor, emptyMessage = 'Nenhum registro encontrado' }: TableProps<T>) {
  return (
    <div style={{ overflowX: 'auto', width: '100%', borderRadius: 'var(--radius-sm)' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
        <thead>
          <tr style={{ background: 'rgba(255, 255, 255, 0.05)', borderBottom: '1px solid var(--border-color)' }}>
            {columns.map((col, index) => (
              <th key={index} style={{ 
                padding: '12px 16px', 
                color: 'var(--text-muted)', 
                fontWeight: 600, 
                fontSize: '0.875rem',
                textTransform: 'uppercase',
                letterSpacing: '0.05em'
              }}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((row) => (
              <tr key={keyExtractor(row)} style={{ 
                borderBottom: '1px solid var(--border-color)',
                transition: 'background 0.2s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.03)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
              >
                {columns.map((col, index) => (
                  <td key={index} style={{ padding: '16px', fontSize: '0.95rem' }}>
                    {typeof col.accessor === 'function' ? col.accessor(row) : (row[col.accessor] as React.ReactNode)}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
