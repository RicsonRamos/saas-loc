interface PaginationControlsProps {
  page: number;
  limit: number;
  total: number;
  onPageChange: (page: number) => void;
}

export function PaginationControls({ page, limit, total, onPageChange }: PaginationControlsProps) {
  const totalPaginas = Math.max(1, Math.ceil(total / limit));

  return (
    <div className="flex items-center justify-between py-3 text-sm text-slate-600">
      <span>
        Página {page} de {totalPaginas} · {total} registro(s)
      </span>
      <div className="flex gap-2">
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={page <= 1}
          className="rounded-md border border-slate-300 px-3 py-1 disabled:opacity-40"
        >
          Anterior
        </button>
        <button
          onClick={() => onPageChange(page + 1)}
          disabled={page >= totalPaginas}
          className="rounded-md border border-slate-300 px-3 py-1 disabled:opacity-40"
        >
          Próxima
        </button>
      </div>
    </div>
  );
}
