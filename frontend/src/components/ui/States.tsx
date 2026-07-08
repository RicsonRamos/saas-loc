export function EmptyState({ mensagem }: { mensagem: string }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-slate-300 py-16 text-slate-500">
      <p>{mensagem}</p>
    </div>
  );
}

export function ErrorState({
  mensagem,
  aoTentarNovamente,
}: {
  mensagem: string;
  aoTentarNovamente?: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-red-200 bg-red-50 py-16 text-red-700">
      <p>{mensagem}</p>
      {aoTentarNovamente && (
        <button onClick={aoTentarNovamente} className="mt-3 text-sm underline">
          Tentar novamente
        </button>
      )}
    </div>
  );
}

export function LoadingState() {
  return (
    <div className="flex items-center justify-center py-16 text-slate-500">
      <span>Carregando...</span>
    </div>
  );
}
