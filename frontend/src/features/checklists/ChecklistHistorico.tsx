import { useQuery } from "@tanstack/react-query";

import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";
import { formatarDataHora } from "@/core/format";

import type { Checklist } from "./checklistTypes";

const ROTULOS_ITEM: Record<string, string> = {
  lataria: "Lataria",
  pneus: "Pneus",
  combustivel: "Combustível",
  km: "Quilometragem",
  documentos: "Documentos",
  acessorios: "Acessórios",
};

const ROTULOS_SITUACAO: Record<string, string> = {
  ok: "OK",
  avaria: "Avaria",
  faltante: "Faltante",
};

const ESTILO_SITUACAO: Record<string, string> = {
  ok: "text-emerald-700",
  avaria: "text-red-700",
  faltante: "text-amber-700",
};

const TITULOS: Record<string, string> = {
  entrega: "Checklist de entrega",
  devolucao: "Checklist de devolução",
};

async function verFoto(attachmentId: string) {
  const { data } = await apiClient.get<{ url: string }>(`/attachments/${attachmentId}/download`);
  window.open(data.url, "_blank");
}

export function ChecklistHistorico({ contratoId }: { contratoId: string }) {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["checklists", contratoId, "historico"],
    queryFn: async () =>
      (
        await apiClient.get<{ data: Checklist[] }>("/checklists", {
          params: { contrato_id: contratoId, limit: 20 },
        })
      ).data.data,
  });

  if (isLoading) return <LoadingState />;
  if (isError) {
    return (
      <ErrorState
        mensagem="Não foi possível carregar o histórico de checklists."
        aoTentarNovamente={() => refetch()}
      />
    );
  }
  if (!data || data.length === 0) {
    return <EmptyState mensagem="Nenhum checklist registrado para este contrato ainda." />;
  }

  return (
    <div className="flex flex-col gap-4">
      {data.map((checklist) => (
        <div key={checklist.id} className="rounded-lg border border-slate-200 bg-white p-4">
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
            <h3 className="text-sm font-semibold text-slate-800">{TITULOS[checklist.tipo]}</h3>
            <span className="text-xs text-slate-500">{formatarDataHora(checklist.data)}</span>
          </div>
          <p className="mb-3 text-xs text-slate-500">
            {checklist.km} km · Combustível: {checklist.combustivel ?? "—"} · Status:{" "}
            {checklist.status}
          </p>
          <ul className="flex flex-col gap-1">
            {checklist.itens.map((item) => (
              <li
                key={item.id}
                className="flex flex-wrap items-center justify-between gap-2 text-sm"
              >
                <span className="text-slate-700">{ROTULOS_ITEM[item.item] ?? item.item}</span>
                <div className="flex items-center gap-3">
                  <span className={`text-xs font-medium ${ESTILO_SITUACAO[item.situacao]}`}>
                    {ROTULOS_SITUACAO[item.situacao] ?? item.situacao}
                  </span>
                  {item.foto_attachment_id && (
                    <button
                      className="text-xs text-blue-700 underline"
                      onClick={() => verFoto(item.foto_attachment_id as string)}
                    >
                      Ver foto
                    </button>
                  )}
                </div>
              </li>
            ))}
          </ul>
          {checklist.observacoes_gerais && (
            <p className="mt-3 text-xs text-slate-500">
              Observações: {checklist.observacoes_gerais}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
