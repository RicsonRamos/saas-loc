import { useQuery } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
import { Link, useParams } from "react-router-dom";

import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { PageHeader } from "@/components/ui/PageHeader";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";
import { formatarData, formatarDataHora, formatarMoeda } from "@/core/format";

import { AbastecimentosSecao } from "./AbastecimentosSecao";
import { AnexosSecao } from "./AnexosSecao";
import { DanosSecao } from "./DanosSecao";
import { HistoricoAuditoriaSecao } from "./HistoricoAuditoriaSecao";
import { LeiturasKmSecao } from "./LeiturasKmSecao";
import { MultasSecao } from "./MultasSecao";
import { PlanosManutencaoSecao } from "./PlanosManutencaoSecao";
import { PneusSecao } from "./PneusSecao";
import { SinistrosSecao } from "./SinistrosSecao";
import { StatusVeiculoBadge } from "./StatusVeiculoBadge";
import type {
  EventoKm,
  HistoricoContrato,
  HistoricoDespesa,
  HistoricoManutencao,
  HistoricoVeiculo,
} from "./historicoTypes";
import type { Veiculo } from "./types";

const contratoColumns = createColumnHelper<HistoricoContrato>();
const manutencaoColumns = createColumnHelper<HistoricoManutencao>();
const despesaColumns = createColumnHelper<HistoricoDespesa>();
const eventoKmColumns = createColumnHelper<EventoKm>();

const ROTULOS_ORIGEM_KM: Record<string, string> = {
  contrato_saida: "Saída em locação",
  contrato_devolucao: "Devolução de locação",
  manutencao: "Manutenção",
  abastecimento: "Abastecimento",
  leitura_km: "Leitura periódica",
};

const colunasEventosKm = [
  eventoKmColumns.accessor("data", { header: "Data", cell: (info) => formatarDataHora(info.getValue()) }),
  eventoKmColumns.accessor("km", { header: "KM registrado" }),
  eventoKmColumns.accessor("origem", {
    header: "Origem",
    cell: (info) => ROTULOS_ORIGEM_KM[info.getValue()] ?? info.getValue(),
  }),
];

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

async function abrirPdf(caminho: string) {
  const { data } = await apiClient.get(caminho, { responseType: "blob" });
  const url = URL.createObjectURL(data as Blob);
  window.open(url, "_blank");
}

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
        <div className="mb-6 flex flex-wrap items-center justify-between gap-3 rounded-lg border border-slate-200 bg-white p-4">
          <div className="flex flex-wrap items-center gap-3">
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
          <div className="flex flex-wrap gap-2">
            <Button variante="secundaria" onClick={() => abrirPdf(`/veiculos/${id}/ficha.pdf`)}>
              Imprimir ficha
            </Button>
            <Button
              variante="secundaria"
              onClick={() => abrirPdf(`/veiculos/${id}/historico.pdf`)}
            >
              Exportar histórico
            </Button>
            <Button
              variante="secundaria"
              onClick={() => abrirPdf(`/veiculos/${id}/abastecimentos.pdf`)}
            >
              Exportar abastecimentos
            </Button>
            <Button
              variante="secundaria"
              onClick={() => abrirPdf(`/veiculos/${id}/manutencoes.pdf`)}
            >
              Exportar manutenções
            </Button>
          </div>
        </div>
      )}

      {!carregando && !comErro && historicoQuery.data && (
        <div className="flex flex-col gap-8">
          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Indicadores
            </h2>
            <div className="grid grid-cols-2 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4">
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">Receita total</p>
                <p className="text-sm font-semibold text-emerald-700">
                  {formatarMoeda(historicoQuery.data.indicadores.receita_total)}
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">Custo total</p>
                <p className="text-sm font-semibold text-red-700">
                  {formatarMoeda(historicoQuery.data.indicadores.custo_total)}
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">Lucro</p>
                <p className="text-sm font-semibold text-slate-900">
                  {formatarMoeda(historicoQuery.data.indicadores.lucro)}
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">Custo por KM</p>
                <p className="text-sm font-semibold text-slate-900">
                  {historicoQuery.data.indicadores.custo_por_km
                    ? formatarMoeda(historicoQuery.data.indicadores.custo_por_km)
                    : "—"}
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">
                  Taxa de utilização
                </p>
                <p className="text-sm font-semibold text-slate-900">
                  {historicoQuery.data.indicadores.taxa_utilizacao}%
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">Dias locado</p>
                <p className="text-sm font-semibold text-slate-900">
                  {historicoQuery.data.indicadores.dias_locado}
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">Dias parado</p>
                <p className="text-sm font-semibold text-slate-900">
                  {historicoQuery.data.indicadores.dias_parado}
                </p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-wide text-slate-500">
                  Dias desde entrada na frota
                </p>
                <p className="text-sm font-semibold text-slate-900">
                  {historicoQuery.data.indicadores.dias_desde_entrada}
                </p>
              </div>
            </div>
          </section>

          {(() => {
            const contratoAtual = historicoQuery.data.contratos.find((c) => c.status === "ativo");
            if (!contratoAtual) return null;
            const dias = Math.max(
              1,
              Math.ceil(
                (Date.now() - new Date(contratoAtual.data_inicio).getTime()) /
                  (1000 * 60 * 60 * 24)
              )
            );
            return (
              <section>
                <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
                  Locação atual
                </h2>
                <div className="grid grid-cols-2 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4">
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">Cliente</p>
                    <p className="text-sm font-semibold text-slate-900">
                      {contratoAtual.cliente_nome}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">Saída</p>
                    <p className="text-sm font-semibold text-slate-900">
                      {formatarDataHora(contratoAtual.data_inicio)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">
                      Devolução prevista
                    </p>
                    <p className="text-sm font-semibold text-slate-900">
                      {formatarDataHora(contratoAtual.data_fim_prevista)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">Diária</p>
                    <p className="text-sm font-semibold text-slate-900">
                      {formatarMoeda(contratoAtual.valor_diaria)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">
                      Dias locado até agora
                    </p>
                    <p className="text-sm font-semibold text-slate-900">{dias}</p>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-wide text-slate-500">KM de saída</p>
                    <p className="text-sm font-semibold text-slate-900">
                      {contratoAtual.km_inicio ?? "—"}
                    </p>
                  </div>
                </div>
              </section>
            );
          })()}

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

          <section>
            <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Quilometragem
            </h2>
            {historicoQuery.data.eventos_km.length === 0 ? (
              <EmptyState mensagem="Nenhum evento de quilometragem registrado ainda." />
            ) : (
              <DataTable columns={colunasEventosKm} data={historicoQuery.data.eventos_km} />
            )}
          </section>

          {id && <LeiturasKmSecao veiculoId={id} />}
          {id && <PlanosManutencaoSecao veiculoId={id} />}
          {id && <AbastecimentosSecao veiculoId={id} />}
          {id && <PneusSecao veiculoId={id} />}
          {id && <MultasSecao veiculoId={id} />}
          {id && <SinistrosSecao veiculoId={id} />}
          {id && <DanosSecao veiculoId={id} />}
          {id && <AnexosSecao veiculoId={id} />}
          {id && <HistoricoAuditoriaSecao veiculoId={id} />}
        </div>
      )}
    </div>
  );
}
