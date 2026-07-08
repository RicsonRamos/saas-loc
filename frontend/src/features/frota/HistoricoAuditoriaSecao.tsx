import { useQuery } from "@tanstack/react-query";
import { useState } from "react";

import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";
import { useAuth } from "@/core/auth/AuthContext";
import { formatarDataHora } from "@/core/format";

import type { AuditLog } from "./auditoriaTypes";

const ROTULOS_ACAO: Record<string, string> = {
  criar: "criou o veículo",
  atualizar: "alterou o veículo",
  excluir: "excluiu o veículo",
  mudar_status: "alterou o status do veículo",
};

function DiffCampos({ log }: { log: AuditLog }) {
  const campos = new Set([
    ...Object.keys(log.dados_anteriores ?? {}),
    ...Object.keys(log.dados_novos ?? {}),
  ]);
  if (campos.size === 0) return null;

  return (
    <dl className="mt-2 grid grid-cols-1 gap-2 text-xs sm:grid-cols-2">
      {Array.from(campos).map((campo) => (
        <div key={campo} className="rounded-md bg-slate-50 p-2">
          <dt className="font-medium text-slate-600">{campo}</dt>
          <dd className="mt-1 flex flex-wrap items-center gap-1 text-slate-800">
            <span className="text-slate-400 line-through">
              {String(log.dados_anteriores?.[campo] ?? "—")}
            </span>
            <span aria-hidden="true">→</span>
            <span className="font-semibold">{String(log.dados_novos?.[campo] ?? "—")}</span>
          </dd>
        </div>
      ))}
    </dl>
  );
}

export function HistoricoAuditoriaSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [expandidoId, setExpandidoId] = useState<string | null>(null);
  const podeVisualizar = hasPermission("auditoria:visualizar");

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["audit-logs", { entidade: "veiculo", entidade_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: AuditLog[] }>("/audit-logs", {
          params: { entidade: "veiculo", entidade_id: veiculoId, limit: 50 },
        })
      ).data.data,
    enabled: podeVisualizar,
  });

  if (!podeVisualizar) return null;

  return (
    <section>
      <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
        Histórico de alterações
      </h2>

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState
          mensagem="Não foi possível carregar o histórico de alterações."
          aoTentarNovamente={() => refetch()}
        />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhuma alteração registrada para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <ol className="flex flex-col gap-3">
          {data.map((log) => (
            <li
              key={log.id}
              className="rounded-lg border border-slate-200 bg-white p-3"
            >
              <button
                type="button"
                className="flex w-full items-center justify-between gap-3 text-left"
                onClick={() => setExpandidoId(expandidoId === log.id ? null : log.id)}
              >
                <span className="text-sm text-slate-800">
                  <span className="font-medium">{formatarDataHora(log.data_hora)}</span>
                  {" — "}
                  {ROTULOS_ACAO[log.acao] ?? log.acao}
                  {log.descricao ? ` (${log.descricao})` : ""}
                </span>
                <span className="text-xs text-slate-400">
                  {expandidoId === log.id ? "ocultar" : "detalhes"}
                </span>
              </button>
              {expandidoId === log.id && <DiffCampos log={log} />}
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}
