import { useQuery } from "@tanstack/react-query";
import { AlertTriangle } from "lucide-react";
import type { ReactNode } from "react";
import { useState } from "react";
import {
  Bar,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Modal } from "@/components/ui/Modal";
import { PageHeader } from "@/components/ui/PageHeader";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";
import { formatarMoeda } from "@/core/format";
import { STATUS_VEICULO_OPCOES } from "@/features/frota/StatusVeiculoBadge";
import type { StatusVeiculo } from "@/features/frota/types";

import { categorizarAlertas, type CategoriaAlertas } from "./alertCategorias";
import type { DashboardResumo, PrioridadeAlerta } from "./types";

const ROTULO_POR_STATUS = Object.fromEntries(
  STATUS_VEICULO_OPCOES.map((opcao) => [opcao.valor, opcao.rotulo])
) as Record<StatusVeiculo, string>;

const ESTILO_POR_PRIORIDADE: Record<PrioridadeAlerta, string> = {
  normal: "border-slate-200 bg-slate-50 text-slate-700",
  atencao: "border-amber-200 bg-amber-50 text-amber-800",
  critico: "border-red-200 bg-red-50 text-red-800",
};

const TILE_POR_PRIORIDADE: Record<PrioridadeAlerta, string> = {
  normal: "border-slate-200 bg-slate-50 hover:bg-slate-100",
  atencao: "border-amber-200 bg-amber-50 hover:bg-amber-100",
  critico: "border-red-200 bg-red-50 hover:bg-red-100",
};

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

function KpiCard({ rotulo, valor, destaque }: { rotulo: string; valor: string; destaque?: string }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">{rotulo}</p>
      <p className={`mt-1 text-xl font-semibold ${destaque ?? "text-slate-900"}`}>{valor}</p>
    </div>
  );
}

function AlertaCategoriaModal({
  categoria,
  aoFechar,
}: {
  categoria: CategoriaAlertas;
  aoFechar: () => void;
}) {
  return (
    <Modal titulo={categoria.rotulo} aoFechar={aoFechar}>
      <ul className="flex flex-col gap-2 text-sm">
        {categoria.alertas.map((alerta, indice) => (
          <li
            key={`${alerta.tipo}-${alerta.veiculo_id ?? indice}`}
            className={`rounded-md border px-3 py-2 ${ESTILO_POR_PRIORIDADE[alerta.prioridade]}`}
          >
            {alerta.mensagem}
          </li>
        ))}
      </ul>
    </Modal>
  );
}

export function DashboardPage() {
  const [categoriaAberta, setCategoriaAberta] = useState<CategoriaAlertas | null>(null);

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["dashboard", "resumo"],
    queryFn: async () => (await apiClient.get<DashboardResumo>("/dashboard/resumo")).data,
  });

  const categorias = data ? categorizarAlertas(data.alertas) : [];

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
        <div className="flex flex-col gap-4">
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
            <KpiCard rotulo="Contratos ativos" valor={String(data.kpis.contratos_ativos)} />
            <KpiCard rotulo="Ocupação da frota" valor={`${data.kpis.taxa_ocupacao.toFixed(1)}%`} />
            {data.kpis.ticket_medio !== null && (
              <KpiCard rotulo="Ticket médio" valor={formatarMoeda(data.kpis.ticket_medio)} />
            )}
            {data.kpis.receita_por_veiculo !== null && (
              <KpiCard rotulo="Receita / veículo" valor={formatarMoeda(data.kpis.receita_por_veiculo)} />
            )}
            <KpiCard
              rotulo="Pagamentos pendentes"
              valor={`${data.kpis.pagamentos_pendentes.quantidade} (${formatarMoeda(
                data.kpis.pagamentos_pendentes.valor
              )})`}
            />
            <KpiCard
              rotulo="Pagamentos atrasados"
              valor={`${data.kpis.pagamentos_atrasados.quantidade} (${formatarMoeda(
                data.kpis.pagamentos_atrasados.valor
              )})`}
              destaque={data.kpis.pagamentos_atrasados.quantidade > 0 ? "text-red-700" : undefined}
            />
          </div>

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

            {data.financeiro_historico && data.financeiro_historico.length > 0 && (
              <Card titulo="💰 Financeiro — últimos meses">
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <ComposedChart data={data.financeiro_historico}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                      <XAxis dataKey="mes" tick={{ fontSize: 12 }} />
                      <YAxis tick={{ fontSize: 12 }} />
                      <Tooltip formatter={(valor) => formatarMoeda(Number(valor))} />
                      <Legend />
                      <Bar dataKey="receita" name="Receita" fill="#059669" radius={[4, 4, 0, 0]} />
                      <Bar dataKey="despesas" name="Despesas" fill="#dc2626" radius={[4, 4, 0, 0]} />
                      <Line
                        type="monotone"
                        dataKey="lucro"
                        name="Lucro"
                        stroke="#0f172a"
                        strokeWidth={2}
                      />
                    </ComposedChart>
                  </ResponsiveContainer>
                </div>
              </Card>
            )}

            <Card titulo="⚠ Alertas">
              {categorias.length === 0 ? (
                <EmptyState mensagem="Nenhum alerta no momento." />
              ) : (
                <div className="grid grid-cols-2 gap-2">
                  {categorias.map((categoria) => (
                    <button
                      key={categoria.chave}
                      type="button"
                      onClick={() => setCategoriaAberta(categoria)}
                      className={`flex flex-col items-start gap-1 rounded-md border px-3 py-2 text-left transition-colors ${TILE_POR_PRIORIDADE[categoria.prioridadeMax]}`}
                    >
                      <span className="flex items-center gap-1 text-xs font-medium uppercase tracking-wide text-slate-600">
                        <AlertTriangle className="h-3.5 w-3.5" />
                        {categoria.rotulo}
                      </span>
                      <span className="text-lg font-semibold text-slate-900">
                        {categoria.alertas.length}
                      </span>
                    </button>
                  ))}
                </div>
              )}
            </Card>
          </div>
        </div>
      )}

      {categoriaAberta && (
        <AlertaCategoriaModal categoria={categoriaAberta} aoFechar={() => setCategoriaAberta(null)} />
      )}
    </div>
  );
}
