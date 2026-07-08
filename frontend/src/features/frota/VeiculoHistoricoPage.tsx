import { useQuery } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
import { Link, useParams } from "react-router-dom";

import { DataTable } from "@/components/ui/DataTable";
import { PageHeader } from "@/components/ui/PageHeader";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";
import { formatarData, formatarDataHora, formatarMoeda } from "@/core/format";

import { StatusVeiculoBadge } from "./StatusVeiculoBadge";
import type {
  HistoricoContrato,
  HistoricoDespesa,
  HistoricoManutencao,
  HistoricoVeiculo,
} from "./historicoTypes";
import type { Veiculo } from "./types";

const contratoColumns = createColumnHelper<HistoricoContrato>();
const manutencaoColumns = createColumnHelper<HistoricoManutencao>();
const despesaColumns = createColumnHelper<HistoricoDespesa>();

const colunasContratos = [
  contratoColumns.accessor("cliente_nome", { header: "Cliente" }),
  contratoColumns.accessor("data_inicio", {
    header: "Saída",
    cell: (info) => formatarDataHora(info.getValue()),
  }),
  contratoColumns.accessor("data_fim_real", {
    header: "Devolução",
    cell: (info) => (info.getValue() ? formatarDataHora(info.getValue() as string) : "—"),
  }),
  contratoColumns.accessor("status", { header: "Status" }),
  contratoColumns.accessor("valor_diaria", {
    header: "Diária",
    cell: (info) => formatarMoeda(info.getValue()),
  }),
  contratoColumns.display({
    id: "km_rodado",
    header: "KM rodada",
    cell: (info) => {
      const { km_inicio, km_final } = info.row.original;
      if (km_inicio == null || km_final == null) return "—";
      return `${km_final - km_inicio} km`;
    },
  }),
];

const colunasManutencoes = [
  manutencaoColumns.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
  manutencaoColumns.accessor("tipo", {
    header: "Tipo",
    cell: (info) => (info.getValue() === "preventiva" ? "Preventiva" : "Corretiva"),
  }),
  manutencaoColumns.accessor("km", { header: "KM" }),
  manutencaoColumns.accessor("custo", { header: "Custo", cell: (info) => formatarMoeda(info.getValue()) }),
  manutencaoColumns.accessor("oficina", { header: "Oficina", cell: (info) => info.getValue() ?? "—" }),
];

const colunasDespesas = [
  despesaColumns.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
  despesaColumns.accessor("categoria", { header: "Categoria" }),
  despesaColumns.accessor("valor", { header: "Valor", cell: (info) => formatarMoeda(info.getValue()) }),
  despesaColumns.accessor("descricao", { header: "Observação", cell: (info) => info.getValue() ?? "—" }),
];

export function VeiculoHistoricoPage() {
  const { id } = useParams<{ id: string }>();

  const veiculoQuery = useQuery({
    queryKey: ["veiculos", id],
    queryFn: async () => (await apiClient.get<Veiculo>(`/veiculos/${id}`)).data,
    enabled: !!id,
  });

  const historicoQuery = useQuery({
    queryKey: ["veiculos", id, "historico"],
    queryFn: async () => (await apiClient.get<HistoricoVeiculo>(`/veiculos/${id}/historico`)).data,
    enabled: !!id,
  });

  const carregando = veiculoQuery.isLoading || historicoQuery.isLoading;
  const comErro = veiculoQuery.isError || historicoQuery.isError;

  return (
    <div>
      <PageHeader
        title="Histórico do veículo"
        actions={
          <Link to="/frota" className="text-sm text-slate-600 underline">
            Voltar para a frota
          </Link>
        }
      />

      {carregando && <LoadingState />}
      {comErro && (
        <ErrorState
          mensagem="Não foi possível carregar o histórico do veículo."
          aoTentarNovamente={() => {
            void veiculoQuery.refetch();
            void historicoQuery.refetch();
          }}
        />
      )}

      {!carregando && !comErro && veiculoQuery.data && (
        <div className="mb-6 flex flex-wrap items-center gap-3 rounded-lg border border-slate-200 bg-white p-4">
          <div>
            <p className="text-lg font-semibold text-slate-900">
              {veiculoQuery.data.placa} — {veiculoQuery.data.modelo}
            </p>
            <p className="text-sm text-slate-500">
              {veiculoQuery.data.marca ?? "—"} · {veiculoQuery.data.ano} · {veiculoQuery.data.km_atual} km
            </p>
          </div>
          <StatusVeiculoBadge status={veiculoQuery.data.status} />
        </div>
      )}

      {!carregando && !comErro && historicoQuery.data && (
        <div className="flex flex-col gap-8">
          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Locações
            </h2>
            {historicoQuery.data.contratos.length === 0 ? (
              <EmptyState mensagem="Nenhuma locação registrada para este veículo." />
            ) : (
              <DataTable columns={colunasContratos} data={historicoQuery.data.contratos} />
            )}
          </section>

          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Manutenções
            </h2>
            {historicoQuery.data.manutencoes.length === 0 ? (
              <EmptyState mensagem="Nenhuma manutenção registrada para este veículo." />
            ) : (
              <DataTable columns={colunasManutencoes} data={historicoQuery.data.manutencoes} />
            )}
          </section>

          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Despesas
            </h2>
            {historicoQuery.data.despesas.length === 0 ? (
              <EmptyState mensagem="Nenhuma despesa registrada para este veículo." />
            ) : (
              <DataTable columns={colunasDespesas} data={historicoQuery.data.despesas} />
            )}
          </section>
        </div>
      )}
    </div>
  );
}
