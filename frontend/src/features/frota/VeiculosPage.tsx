import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
import { History, Pencil, Trash2, Wrench } from "lucide-react";
import type { ReactNode } from "react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";

import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { PageHeader } from "@/components/ui/PageHeader";
import { PaginationControls } from "@/components/ui/PaginationControls";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient, extrairMensagemErro } from "@/core/api/client";
import { useAuth } from "@/core/auth/AuthContext";
import { usePaginatedQuery } from "@/core/hooks/usePaginatedQuery";

import { veiculoSchema, type VeiculoFormInput, type VeiculoFormValues } from "./schema";
import { STATUS_VEICULO_OPCOES, StatusVeiculoBadge } from "./StatusVeiculoBadge";
import type { Veiculo } from "./types";

const columnHelper = createColumnHelper<Veiculo>();

const BOTAO_ACAO_BASE =
  "inline-flex h-7 w-7 items-center justify-center rounded-md border transition-colors";

const CORES_ACAO = {
  slate: "border-slate-200 text-slate-600 hover:bg-slate-100 hover:text-slate-900",
  blue: "border-blue-200 text-blue-600 hover:bg-blue-50 hover:text-blue-800",
  amber: "border-amber-200 text-amber-600 hover:bg-amber-50 hover:text-amber-800",
  red: "border-red-200 text-red-600 hover:bg-red-50 hover:text-red-800",
} as const;

// licenciamento_vencido/seguro_vencido são calculados automaticamente pelo backend
// (ver veiculo_service.calcular_status_efetivo) e não devem ser escolhidos manualmente.
const OPCOES_STATUS_MANUAL = STATUS_VEICULO_OPCOES.filter(
  (opcao) => opcao.valor !== "licenciamento_vencido" && opcao.valor !== "seguro_vencido"
);

const CAMPOS_VAZIOS: VeiculoFormInput = {
  placa: "",
  modelo: "",
  ano: 0,
  km_atual: 0,
  marca: "",
  cor: "",
  categoria: "",
  chassi: "",
  renavam: "",
  combustivel: "",
  cambio: "",
  vencimento_licenciamento: "",
  vencimento_seguro: "",
  status: "",
  versao: "",
  ano_fabricacao: "",
  portas: "",
  capacidade_passageiros: "",
  motor: "",
  potencia: "",
  data_aquisicao: "",
  valor_compra: "",
  fornecedor: "",
  forma_aquisicao: "",
  km_inicial: "",
  proprietario: "",
  data_entrada_frota: "",
  garantia_fabrica_ate: "",
  garantia_concessionaria_ate: "",
  crlv_numero: "",
  ipva_vencimento: "",
  alienado: false,
  alienante: "",
  seguradora: "",
  apolice_numero: "",
  seguro_franquia: "",
  seguro_cobertura: "",
  seguro_contato: "",
};

function Campo({ label, children }: { label: string; children: ReactNode }) {
  return (
    <div>
      <label className="mb-1 block text-sm font-medium text-slate-700">{label}</label>
      {children}
    </div>
  );
}

const inputClasse =
  "w-full rounded-md border border-slate-300 px-3 py-2 text-sm disabled:bg-slate-100";

export function VeiculosPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [busca, setBusca] = useState("");
  const [filtroMarca, setFiltroMarca] = useState("");
  const [filtroCategoria, setFiltroCategoria] = useState("");
  const [filtroAno, setFiltroAno] = useState("");
  const [filtroStatus, setFiltroStatus] = useState("");
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Veiculo>(
    ["veiculos"],
    "/veiculos",
    {
      page,
      limit,
      busca: busca || undefined,
      marca: filtroMarca || undefined,
      categoria: filtroCategoria || undefined,
      ano: filtroAno || undefined,
      status: filtroStatus || undefined,
    }
  );

  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<VeiculoFormInput, unknown, VeiculoFormValues>({
    resolver: zodResolver(veiculoSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["veiculos"] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(veiculo: Veiculo) {
    setEditandoId(veiculo.id);
    reset({
      placa: veiculo.placa,
      modelo: veiculo.modelo,
      ano: veiculo.ano,
      km_atual: veiculo.km_atual,
      marca: veiculo.marca ?? "",
      cor: veiculo.cor ?? "",
      categoria: veiculo.categoria ?? "",
      chassi: veiculo.chassi ?? "",
      renavam: veiculo.renavam ?? "",
      combustivel: veiculo.combustivel ?? "",
      cambio: veiculo.cambio ?? "",
      vencimento_licenciamento: veiculo.vencimento_licenciamento ?? "",
      vencimento_seguro: veiculo.vencimento_seguro ?? "",
      status: veiculo.status,
      versao: veiculo.versao ?? "",
      ano_fabricacao: veiculo.ano_fabricacao != null ? String(veiculo.ano_fabricacao) : "",
      portas: veiculo.portas != null ? String(veiculo.portas) : "",
      capacidade_passageiros:
        veiculo.capacidade_passageiros != null ? String(veiculo.capacidade_passageiros) : "",
      motor: veiculo.motor ?? "",
      potencia: veiculo.potencia ?? "",
      data_aquisicao: veiculo.data_aquisicao ?? "",
      valor_compra: veiculo.valor_compra ?? "",
      fornecedor: veiculo.fornecedor ?? "",
      forma_aquisicao: veiculo.forma_aquisicao ?? "",
      km_inicial: veiculo.km_inicial != null ? String(veiculo.km_inicial) : "",
      proprietario: veiculo.proprietario ?? "",
      data_entrada_frota: veiculo.data_entrada_frota ?? "",
      garantia_fabrica_ate: veiculo.garantia_fabrica_ate ?? "",
      garantia_concessionaria_ate: veiculo.garantia_concessionaria_ate ?? "",
      crlv_numero: veiculo.crlv_numero ?? "",
      ipva_vencimento: veiculo.ipva_vencimento ?? "",
      alienado: veiculo.alienado,
      alienante: veiculo.alienante ?? "",
      seguradora: veiculo.seguradora ?? "",
      apolice_numero: veiculo.apolice_numero ?? "",
      seguro_franquia: veiculo.seguro_franquia ?? "",
      seguro_cobertura: veiculo.seguro_cobertura ?? "",
      seguro_contato: veiculo.seguro_contato ?? "",
    });
    setErroForm(null);
    setMostrarForm(true);
  }

  function fecharForm() {
    setMostrarForm(false);
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
  }

  const criarVeiculo = useMutation({
    mutationFn: (valores: VeiculoFormValues) => apiClient.post("/veiculos", valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizarVeiculo = useMutation({
    mutationFn: (valores: VeiculoFormValues) =>
      apiClient.patch(`/veiculos/${editandoId}`, valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const removerVeiculo = useMutation({
    mutationFn: (veiculoId: string) => apiClient.delete(`/veiculos/${veiculoId}`),
    onSuccess: () => {
      invalidar();
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  const acaoRapida = useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Record<string, unknown> }) =>
      apiClient.patch(`/veiculos/${id}`, payload),
    onSuccess: () => {
      invalidar();
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  function excluir(veiculo: Veiculo) {
    if (window.confirm(`Excluir o veículo ${veiculo.placa}?`)) {
      removerVeiculo.mutate(veiculo.id);
    }
  }

  function enviarParaManutencao(veiculo: Veiculo) {
    if (window.confirm(`Enviar o veículo ${veiculo.placa} para manutenção?`)) {
      acaoRapida.mutate({ id: veiculo.id, payload: { status: "em_manutencao" } });
    }
  }

  const podeEditar = hasPermission("frota:editar");

  const columns = [
    columnHelper.accessor("placa", { header: "Placa" }),
    columnHelper.accessor("modelo", { header: "Modelo" }),
    columnHelper.accessor("marca", { header: "Marca", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("ano", { header: "Ano" }),
    columnHelper.accessor("cor", { header: "Cor", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("categoria", {
      header: "Categoria",
      cell: (info) => info.getValue() ?? "—",
    }),
    columnHelper.accessor("km_atual", { header: "KM atual" }),
    columnHelper.accessor("status", {
      header: "Situação",
      cell: (info) => <StatusVeiculoBadge status={info.getValue()} />,
    }),
    columnHelper.display({
      id: "acoes",
      header: "Ações",
      cell: (info: { row: { original: Veiculo } }) => {
        const veiculo = info.row.original;
        return (
          <div className="flex flex-wrap gap-1.5">
            <Link
              className={`${BOTAO_ACAO_BASE} ${CORES_ACAO.slate}`}
              to={`/frota/${veiculo.id}`}
              title="Histórico"
              aria-label="Histórico"
            >
              <History className="h-3.5 w-3.5" />
            </Link>
            {podeEditar && (
              <>
                <button
                  type="button"
                  className={`${BOTAO_ACAO_BASE} ${CORES_ACAO.blue}`}
                  onClick={() => abrirEdicao(veiculo)}
                  title="Editar"
                  aria-label="Editar"
                >
                  <Pencil className="h-3.5 w-3.5" />
                </button>
                {veiculo.status !== "em_manutencao" && (
                  <button
                    type="button"
                    className={`${BOTAO_ACAO_BASE} ${CORES_ACAO.amber}`}
                    onClick={() => enviarParaManutencao(veiculo)}
                    title="Enviar p/ manutenção"
                    aria-label="Enviar para manutenção"
                  >
                    <Wrench className="h-3.5 w-3.5" />
                  </button>
                )}
                <button
                  type="button"
                  className={`${BOTAO_ACAO_BASE} ${CORES_ACAO.red}`}
                  onClick={() => excluir(veiculo)}
                  title="Excluir"
                  aria-label="Excluir"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              </>
            )}
          </div>
        );
      },
    }),
  ];

  return (
    <div>
      <PageHeader
        title="Frota"
        actions={
          podeEditar && (
            <Button onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}>
              {mostrarForm ? "Cancelar" : "Novo veículo"}
            </Button>
          )
        }
      />

      <div className="mb-4 grid grid-cols-1 gap-3 sm:grid-cols-5">
        <input
          className={inputClasse}
          placeholder="Buscar por placa, modelo ou chassi..."
          value={busca}
          onChange={(evento) => {
            setBusca(evento.target.value);
            setPage(1);
          }}
        />
        <input
          className={inputClasse}
          placeholder="Marca"
          value={filtroMarca}
          onChange={(evento) => {
            setFiltroMarca(evento.target.value);
            setPage(1);
          }}
        />
        <input
          className={inputClasse}
          placeholder="Categoria"
          value={filtroCategoria}
          onChange={(evento) => {
            setFiltroCategoria(evento.target.value);
            setPage(1);
          }}
        />
        <input
          className={inputClasse}
          placeholder="Ano"
          type="number"
          value={filtroAno}
          onChange={(evento) => {
            setFiltroAno(evento.target.value);
            setPage(1);
          }}
        />
        <select
          className={inputClasse}
          value={filtroStatus}
          onChange={(evento) => {
            setFiltroStatus(evento.target.value);
            setPage(1);
          }}
        >
          <option value="">Todas as situações</option>
          {STATUS_VEICULO_OPCOES.map((opcao) => (
            <option key={opcao.valor} value={opcao.valor}>
              {opcao.rotulo}
            </option>
          ))}
        </select>
      </div>

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) =>
            editandoId ? atualizarVeiculo.mutate(valores) : criarVeiculo.mutate(valores)
          )}
          className="mb-6 flex flex-col gap-6 rounded-lg border border-slate-200 bg-white p-4"
        >
          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Identificação
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="Placa">
                <input className={inputClasse} disabled={!!editandoId} {...register("placa")} />
                {errors.placa && <p className="text-xs text-red-600">{errors.placa.message}</p>}
              </Campo>
              <Campo label="Modelo">
                <input className={inputClasse} {...register("modelo")} />
                {errors.modelo && <p className="text-xs text-red-600">{errors.modelo.message}</p>}
              </Campo>
              <Campo label="Marca">
                <input className={inputClasse} {...register("marca")} />
              </Campo>
              <Campo label="Versão">
                <input className={inputClasse} {...register("versao")} />
              </Campo>
              <Campo label="Ano modelo">
                <input type="number" className={inputClasse} {...register("ano")} />
                {errors.ano && <p className="text-xs text-red-600">{errors.ano.message}</p>}
              </Campo>
              <Campo label="Ano de fabricação">
                <input type="number" className={inputClasse} {...register("ano_fabricacao")} />
              </Campo>
              <Campo label="Cor">
                <input className={inputClasse} {...register("cor")} />
              </Campo>
              <Campo label="Categoria">
                <input
                  className={inputClasse}
                  placeholder="Ex.: Hatch, SUV, Pickup"
                  {...register("categoria")}
                />
              </Campo>
              <Campo label="Combustível">
                <input className={inputClasse} {...register("combustivel")} />
              </Campo>
              <Campo label="Câmbio">
                <input className={inputClasse} {...register("cambio")} />
              </Campo>
              <Campo label="Portas">
                <input type="number" className={inputClasse} {...register("portas")} />
              </Campo>
              <Campo label="Capacidade de passageiros">
                <input
                  type="number"
                  className={inputClasse}
                  {...register("capacidade_passageiros")}
                />
              </Campo>
              <Campo label="Motor">
                <input className={inputClasse} {...register("motor")} />
              </Campo>
              <Campo label="Potência">
                <input className={inputClasse} {...register("potencia")} />
              </Campo>
              <Campo label="KM atual">
                <input type="number" className={inputClasse} {...register("km_atual")} />
              </Campo>
              <Campo label="Chassi">
                <input className={inputClasse} {...register("chassi")} />
              </Campo>
              <Campo label="RENAVAM">
                <input className={inputClasse} {...register("renavam")} />
              </Campo>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Dados de aquisição
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="Data de aquisição">
                <input type="date" className={inputClasse} {...register("data_aquisicao")} />
              </Campo>
              <Campo label="Valor de compra">
                <input
                  type="number"
                  step="0.01"
                  className={inputClasse}
                  {...register("valor_compra")}
                />
              </Campo>
              <Campo label="Fornecedor">
                <input className={inputClasse} {...register("fornecedor")} />
              </Campo>
              <Campo label="Forma de aquisição">
                <input
                  className={inputClasse}
                  placeholder="Ex.: À vista, Financiado"
                  {...register("forma_aquisicao")}
                />
              </Campo>
              <Campo label="KM inicial">
                <input type="number" className={inputClasse} {...register("km_inicial")} />
              </Campo>
              <Campo label="Proprietário">
                <input className={inputClasse} {...register("proprietario")} />
              </Campo>
              <Campo label="Data de entrada na frota">
                <input type="date" className={inputClasse} {...register("data_entrada_frota")} />
              </Campo>
              <Campo label="Garantia de fábrica até">
                <input type="date" className={inputClasse} {...register("garantia_fabrica_ate")} />
              </Campo>
              <Campo label="Garantia da concessionária até">
                <input
                  type="date"
                  className={inputClasse}
                  {...register("garantia_concessionaria_ate")}
                />
              </Campo>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Documentação
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="CRLV (número)">
                <input className={inputClasse} {...register("crlv_numero")} />
              </Campo>
              <Campo label="Vencimento do IPVA">
                <input type="date" className={inputClasse} {...register("ipva_vencimento")} />
              </Campo>
              <Campo label="Vencimento do licenciamento">
                <input
                  type="date"
                  className={inputClasse}
                  {...register("vencimento_licenciamento")}
                />
              </Campo>
              <div className="flex items-end gap-2">
                <input type="checkbox" id="alienado" {...register("alienado")} />
                <label htmlFor="alienado" className="text-sm text-slate-700">
                  Veículo alienado
                </label>
              </div>
              <Campo label="Alienante (banco/financeira)">
                <input className={inputClasse} {...register("alienante")} />
              </Campo>
            </div>
          </fieldset>

          <fieldset>
            <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
              Seguro
            </legend>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
              <Campo label="Seguradora">
                <input className={inputClasse} {...register("seguradora")} />
              </Campo>
              <Campo label="Nº da apólice">
                <input className={inputClasse} {...register("apolice_numero")} />
              </Campo>
              <Campo label="Franquia">
                <input
                  type="number"
                  step="0.01"
                  className={inputClasse}
                  {...register("seguro_franquia")}
                />
              </Campo>
              <Campo label="Vencimento do seguro">
                <input type="date" className={inputClasse} {...register("vencimento_seguro")} />
              </Campo>
              <Campo label="Contato da seguradora">
                <input className={inputClasse} {...register("seguro_contato")} />
              </Campo>
              <div className="sm:col-span-3">
                <Campo label="Coberturas">
                  <input className={inputClasse} {...register("seguro_cobertura")} />
                </Campo>
              </div>
            </div>
          </fieldset>

          {editandoId && (
            <fieldset>
              <legend className="mb-2 text-sm font-semibold uppercase tracking-wide text-slate-500">
                Situação
              </legend>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
                <Campo label="Situação">
                  <select className={inputClasse} {...register("status")}>
                    {OPCOES_STATUS_MANUAL.map((opcao) => (
                      <option key={opcao.valor} value={opcao.valor}>
                        {opcao.rotulo}
                      </option>
                    ))}
                  </select>
                </Campo>
              </div>
            </fieldset>
          )}

          {erroForm && <p className="text-sm text-red-600">{erroForm}</p>}
          <div>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar veículo" : "Salvar veículo"}
            </Button>
          </div>
        </form>
      )}

      {erroAcao && <p className="mb-3 text-sm text-red-600">{erroAcao}</p>}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState
          mensagem="Não foi possível carregar a frota."
          aoTentarNovamente={() => refetch()}
        />
      )}
      {!isLoading && !isError && data && data.data.length === 0 && (
        <EmptyState mensagem="Nenhum veículo cadastrado ainda." />
      )}
      {!isLoading && !isError && data && data.data.length > 0 && (
        <>
          <DataTable columns={columns} data={data.data} />
          <PaginationControls
            page={data.meta.page}
            limit={data.meta.limit}
            total={data.meta.total}
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
}
