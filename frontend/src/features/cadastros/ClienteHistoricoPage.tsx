import { useQuery } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
import { Link, useParams } from "react-router-dom";

import { DataTable } from "@/components/ui/DataTable";
import { PageHeader } from "@/components/ui/PageHeader";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";
import { formatarData, formatarDataHora, formatarMoeda } from "@/core/format";

import type { Dano, Multa, Sinistro } from "@/features/frota/incidentesTypes";

import { CondutoresSecao } from "./CondutoresSecao";
import { StatusClienteBadge } from "./StatusClienteBadge";
import type { HistoricoCliente, HistoricoLocacaoCliente } from "./clienteHistoricoTypes";
import type { Cliente, StatusCliente } from "./types";

const locacaoColumns = createColumnHelper<HistoricoLocacaoCliente>();
const multaColumns = createColumnHelper<Multa>();
const sinistroColumns = createColumnHelper<Sinistro>();
const danoColumns = createColumnHelper<Dano>();

const ROTULOS_TIPO_SINISTRO: Record<string, string> = {
  batida: "Batida",
  roubo: "Roubo",
  furto: "Furto",
  enchente: "Enchente",
  incendio: "Incêndio",
};

const ROTULOS_TIPO_DANO: Record<string, string> = {
  arranhao: "Arranhão",
  amassado: "Amassado",
  quebra_vidro: "Quebra de vidro",
  dano_interno: "Dano interno",
  outro: "Outro",
};

const colunasMultas = [
  multaColumns.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
  multaColumns.accessor("infracao", { header: "Infração" }),
  multaColumns.accessor("valor", { header: "Valor", cell: (info) => formatarMoeda(info.getValue()) }),
  multaColumns.accessor("status", { header: "Situação" }),
];

const colunasSinistros = [
  sinistroColumns.accessor("data", {
    header: "Data",
    cell: (info) => formatarDataHora(info.getValue()),
  }),
  sinistroColumns.accessor("tipo", {
    header: "Tipo",
    cell: (info) => ROTULOS_TIPO_SINISTRO[info.getValue()],
  }),
  sinistroColumns.accessor("descricao", { header: "Descrição", cell: (info) => info.getValue() ?? "—" }),
  sinistroColumns.accessor("status", { header: "Situação" }),
];

const colunasDanos = [
  danoColumns.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
  danoColumns.accessor("tipo", { header: "Tipo", cell: (info) => ROTULOS_TIPO_DANO[info.getValue()] }),
  danoColumns.accessor("descricao", { header: "Descrição", cell: (info) => info.getValue() ?? "—" }),
  danoColumns.accessor("status", { header: "Situação" }),
];

const colunasLocacoes = [
  locacaoColumns.accessor("veiculo_placa", { header: "Veículo" }),
  locacaoColumns.accessor("data_inicio", {
    header: "Retirada",
    cell: (info) => formatarDataHora(info.getValue()),
  }),
  locacaoColumns.accessor("data_fim_real", {
    header: "Devolução",
    cell: (info) => (info.getValue() ? formatarDataHora(info.getValue() as string) : "—"),
  }),
  locacaoColumns.accessor("valor_diaria", {
    header: "Valor",
    cell: (info) => formatarMoeda(info.getValue()),
  }),
  locacaoColumns.accessor("status", { header: "Status" }),
  locacaoColumns.display({
    id: "km_rodado",
    header: "Quilometragem",
    cell: (info) => {
      const { km_inicio, km_final } = info.row.original;
      if (km_inicio == null || km_final == null) return "—";
      return `${km_final - km_inicio} km`;
    },
  }),
];

function estrelas(quantidade: number): string {
  return "⭐".repeat(quantidade) + "☆".repeat(5 - quantidade);
}

function CardResumo({ titulo, valor }: { titulo: string; valor: string }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-3">
      <p className="text-xs uppercase tracking-wide text-slate-500">{titulo}</p>
      <p className="mt-1 text-sm font-semibold text-slate-900">{valor}</p>
    </div>
  );
}

export function ClienteHistoricoPage() {
  const { id } = useParams<{ id: string }>();

  const clienteQuery = useQuery({
    queryKey: ["clientes", id],
    queryFn: async () => (await apiClient.get<Cliente>(`/clientes/${id}`)).data,
    enabled: !!id,
  });

  const historicoQuery = useQuery({
    queryKey: ["clientes", id, "historico"],
    queryFn: async () => (await apiClient.get<HistoricoCliente>(`/clientes/${id}/historico`)).data,
    enabled: !!id,
  });

  const carregando = clienteQuery.isLoading || historicoQuery.isLoading;
  const comErro = clienteQuery.isError || historicoQuery.isError;

  return (
    <div>
      <PageHeader
        title="Ficha do cliente"
        actions={
          <Link to="/clientes" className="text-sm text-slate-600 underline">
            Voltar para clientes
          </Link>
        }
      />

      {carregando && <LoadingState />}
      {comErro && (
        <ErrorState
          mensagem="Não foi possível carregar a ficha do cliente."
          aoTentarNovamente={() => {
            void clienteQuery.refetch();
            void historicoQuery.refetch();
          }}
        />
      )}

      {!carregando && !comErro && clienteQuery.data && (
        <div className="mb-6 flex flex-wrap items-center gap-3 rounded-lg border border-slate-200 bg-white p-4">
          <div>
            <p className="text-lg font-semibold text-slate-900">{clienteQuery.data.nome}</p>
            <p className="text-sm text-slate-500">{clienteQuery.data.documento}</p>
          </div>
          <StatusClienteBadge status={clienteQuery.data.status as StatusCliente} />
        </div>
      )}

      {!carregando && !comErro && historicoQuery.data && (
        <div className="flex flex-col gap-8">
          <section>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <CardResumo
                titulo="CNH"
                valor={
                  historicoQuery.data.ficha.cnh_categoria
                    ? `Categoria ${historicoQuery.data.ficha.cnh_categoria}`
                    : "—"
                }
              />
              <CardResumo
                titulo="CNH vence em"
                valor={
                  historicoQuery.data.ficha.cnh_vencimento
                    ? formatarData(historicoQuery.data.ficha.cnh_vencimento)
                    : "—"
                }
              />
              <CardResumo
                titulo="Locações realizadas"
                valor={String(historicoQuery.data.ficha.locacoes_realizadas)}
              />
              <CardResumo
                titulo="Locação atual"
                valor={
                  historicoQuery.data.ficha.locacao_atual
                    ? (historicoQuery.data.ficha.veiculo_atual_modelo ?? "Sim")
                    : "Nenhuma"
                }
              />
              <CardResumo
                titulo="Valor total gasto"
                valor={formatarMoeda(historicoQuery.data.ficha.valor_total_gasto)}
              />
              <CardResumo
                titulo="Pendências"
                valor={formatarMoeda(historicoQuery.data.ficha.pendencias)}
              />
              <CardResumo
                titulo="Avaliação"
                valor={estrelas(historicoQuery.data.ficha.avaliacao_estrelas)}
              />
            </div>
          </section>

          {historicoQuery.data.alertas.length > 0 && (
            <section>
              <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
                Alertas
              </h2>
              <ul className="flex flex-col gap-1 text-sm">
                {historicoQuery.data.alertas.map((alerta, indice) => (
                  <li key={`${alerta.tipo}-${indice}`}>⚠ {alerta.mensagem}</li>
                ))}
              </ul>
            </section>
          )}

          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Histórico de locações
            </h2>
            {historicoQuery.data.locacoes.length === 0 ? (
              <EmptyState mensagem="Nenhuma locação registrada para este cliente." />
            ) : (
              <DataTable columns={colunasLocacoes} data={historicoQuery.data.locacoes} />
            )}
          </section>

          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Histórico financeiro
            </h2>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <CardResumo
                titulo="Total pago"
                valor={formatarMoeda(historicoQuery.data.financeiro.total_pago)}
              />
              <CardResumo
                titulo="Total em aberto"
                valor={formatarMoeda(historicoQuery.data.financeiro.total_pendente)}
              />
              <CardResumo
                titulo="Total estornado"
                valor={formatarMoeda(historicoQuery.data.financeiro.total_estornado)}
              />
            </div>
          </section>

          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Multas
            </h2>
            {historicoQuery.data.multas.length === 0 ? (
              <EmptyState mensagem="Nenhuma multa registrada para este cliente." />
            ) : (
              <DataTable columns={colunasMultas} data={historicoQuery.data.multas} />
            )}
          </section>

          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Sinistros
            </h2>
            {historicoQuery.data.sinistros.length === 0 ? (
              <EmptyState mensagem="Nenhum sinistro registrado para este cliente." />
            ) : (
              <DataTable columns={colunasSinistros} data={historicoQuery.data.sinistros} />
            )}
          </section>

          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Danos
            </h2>
            {historicoQuery.data.danos.length === 0 ? (
              <EmptyState mensagem="Nenhum dano registrado para este cliente." />
            ) : (
              <DataTable columns={colunasDanos} data={historicoQuery.data.danos} />
            )}
          </section>

          {id && <CondutoresSecao clienteId={id} />}
        </div>
      )}
    </div>
  );
}
