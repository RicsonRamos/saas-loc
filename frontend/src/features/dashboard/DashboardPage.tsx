import { useQuery } from "@tanstack/react-query";
import type { ReactNode } from "react";

import { PageHeader } from "@/components/ui/PageHeader";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";
import { formatarMoeda } from "@/core/format";
import { STATUS_VEICULO_OPCOES } from "@/features/frota/StatusVeiculoBadge";
import type { StatusVeiculo } from "@/features/frota/types";

import type { DashboardResumo } from "./types";

const ROTULO_POR_STATUS = Object.fromEntries(
  STATUS_VEICULO_OPCOES.map((opcao) => [opcao.valor, opcao.rotulo])
) as Record<StatusVeiculo, string>;

function Card({ titulo, children }: { titulo: string; children: ReactNode }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500">
        {titulo}
      </h2>
      {children}
    </div>
  );
}

export function DashboardPage() {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["dashboard", "resumo"],
    queryFn: async () => (await apiClient.get<DashboardResumo>("/dashboard/resumo")).data,
  });

  return (
    <div>
      <PageHeader title="Dashboard" />

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState
          mensagem="Não foi possível carregar o dashboard."
          aoTentarNovamente={() => refetch()}
        />
      )}

      {!isLoading && !isError && data && (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <Card titulo="🚗 Veículos">
            {Object.keys(data.veiculos_por_status).length === 0 ? (
              <EmptyState mensagem="Nenhum veículo cadastrado ainda." />
            ) : (
              <ul className="flex flex-col gap-2">
                {Object.entries(data.veiculos_por_status).map(([status, total]) => (
                  <li key={status} className="flex items-center justify-between text-sm">
                    <span>{ROTULO_POR_STATUS[status as StatusVeiculo] ?? status}</span>
                    <span className="font-semibold text-slate-900">{total}</span>
                  </li>
                ))}
              </ul>
            )}
          </Card>

          <Card titulo="📅 Vencimentos">
            <ul className="flex flex-col gap-2 text-sm">
              <li className="flex items-center justify-between">
                <span>Seguro (próx. 30 dias)</span>
                <span className="font-semibold text-slate-900">
                  {data.vencimentos.seguro_30_dias}
                </span>
              </li>
              <li className="flex items-center justify-between">
                <span>Licenciamento (próx. 30 dias)</span>
                <span className="font-semibold text-slate-900">
                  {data.vencimentos.licenciamento_30_dias}
                </span>
              </li>
            </ul>
          </Card>

          {data.financeiro_mes && (
            <Card titulo="💰 Financeiro do mês">
              <ul className="flex flex-col gap-2 text-sm">
                <li className="flex items-center justify-between">
                  <span>Receita</span>
                  <span className="font-semibold text-emerald-700">
                    {formatarMoeda(data.financeiro_mes.receita)}
                  </span>
                </li>
                <li className="flex items-center justify-between">
                  <span>Despesas</span>
                  <span className="font-semibold text-red-700">
                    {formatarMoeda(data.financeiro_mes.despesas)}
                  </span>
                </li>
                <li className="flex items-center justify-between border-t border-slate-100 pt-2">
                  <span>Lucro</span>
                  <span className="font-semibold text-slate-900">
                    {formatarMoeda(data.financeiro_mes.lucro)}
                  </span>
                </li>
              </ul>
            </Card>
          )}

          <Card titulo="⚠ Alertas">
            {data.alertas.length === 0 ? (
              <EmptyState mensagem="Nenhum alerta no momento." />
            ) : (
              <ul className="flex flex-col gap-2 text-sm">
                {data.alertas.map((alerta, indice) => (
                  <li key={`${alerta.tipo}-${alerta.veiculo_id ?? indice}`}>
                    • {alerta.mensagem}
                  </li>
                ))}
              </ul>
            )}
          </Card>
        </div>
      )}
    </div>
  );
}
