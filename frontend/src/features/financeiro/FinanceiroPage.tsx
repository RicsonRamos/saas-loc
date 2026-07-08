import { zodResolver } from "@hookform/resolvers/zod";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { PageHeader } from "@/components/ui/PageHeader";
import { PaginationControls } from "@/components/ui/PaginationControls";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient, extrairMensagemErro } from "@/core/api/client";
import { useAuth } from "@/core/auth/AuthContext";
import { formatarData, formatarMoeda } from "@/core/format";
import { usePaginatedQuery } from "@/core/hooks/usePaginatedQuery";
import type { Contrato } from "@/features/contratos/types";
import type { Veiculo } from "@/features/frota/types";

import {
  despesaSchema,
  pagamentoSchema,
  type DespesaFormInput,
  type DespesaFormValues,
  type PagamentoFormInput,
  type PagamentoFormValues,
} from "./schema";
import { RentabilidadeChart } from "./RentabilidadeChart";
import type { Despesa, Pagamento, RentabilidadeVeiculo } from "./types";

type Aba = "pagamentos" | "despesas" | "rentabilidade";

export function FinanceiroPage() {
  const [aba, setAba] = useState<Aba>("pagamentos");

  return (
    <div>
      <PageHeader title="Financeiro" />

      <div className="mb-6 flex gap-2 border-b border-slate-200">
        {(
          [
            ["pagamentos", "Pagamentos"],
            ["despesas", "Despesas"],
            ["rentabilidade", "Rentabilidade"],
          ] as [Aba, string][]
        ).map(([valor, rotulo]) => (
          <button
            key={valor}
            onClick={() => setAba(valor)}
            className={`-mb-px border-b-2 px-3 py-2 text-sm font-medium ${
              aba === valor ? "border-slate-900 text-slate-900" : "border-transparent text-slate-500"
            }`}
          >
            {rotulo}
          </button>
        ))}
      </div>

      {aba === "pagamentos" && <PagamentosTab />}
      {aba === "despesas" && <DespesasTab />}
      {aba === "rentabilidade" && <RentabilidadeTab />}
    </div>
  );
}

function PagamentosTab() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Pagamento>(
    ["financeiro", "pagamentos"],
    "/financeiro/pagamentos",
    { page, limit }
  );
  const { data: contratos } = usePaginatedQuery<Contrato>(["contratos", "select"], "/contratos", {
    page: 1,
    limit: 100,
  });

  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<PagamentoFormInput, unknown, PagamentoFormValues>({
    resolver: zodResolver(pagamentoSchema),
  });

  const lancarPagamento = useMutation({
    mutationFn: (valores: PagamentoFormValues) =>
      apiClient.post("/financeiro/pagamentos", { ...valores, data: `${valores.data}T00:00:00Z` }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["financeiro", "pagamentos"] });
      reset();
      setMostrarForm(false);
      setErroForm(null);
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const estornarPagamento = useMutation({
    mutationFn: (pagamentoId: string) =>
      apiClient.patch(`/financeiro/pagamentos/${pagamentoId}/estorno`),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["financeiro", "pagamentos"] });
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  const columnHelper = createColumnHelper<Pagamento>();
  const columns = [
    columnHelper.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
    columnHelper.accessor("valor", { header: "Valor", cell: (info) => formatarMoeda(info.getValue()) }),
    columnHelper.accessor("metodo", { header: "Método", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("status", { header: "Status" }),
    columnHelper.display({
      id: "acoes",
      header: "Ações",
      cell: (info) => {
        const pagamento = info.row.original;
        if (pagamento.status !== "pago" || !hasPermission("financeiro:aprovar_estorno")) return null;
        return (
          <button
            className="text-xs text-red-700 underline"
            onClick={() => estornarPagamento.mutate(pagamento.id)}
          >
            Estornar
          </button>
        );
      },
    }),
  ];

  const podeLancar = hasPermission("financeiro:lancar");

  return (
    <div>
      {podeLancar && (
        <div className="mb-4">
          <Button onClick={() => setMostrarForm((v) => !v)}>
            {mostrarForm ? "Cancelar" : "Lançar pagamento"}
          </Button>
        </div>
      )}

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) => lancarPagamento.mutate(valores))}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Contrato</label>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("contrato_id")}
            >
              <option value="">Selecione...</option>
              {contratos?.data.map((contrato) => (
                <option key={contrato.id} value={contrato.id}>
                  {contrato.id.slice(0, 8)}…
                </option>
              ))}
            </select>
            {errors.contrato_id && <p className="text-xs text-red-600">{errors.contrato_id.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Valor</label>
            <input
              type="number"
              step="0.01"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("valor")}
            />
            {errors.valor && <p className="text-xs text-red-600">{errors.valor.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Data</label>
            <input
              type="date"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("data")}
            />
            {errors.data && <p className="text-xs text-red-600">{errors.data.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Método</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("metodo")}
            />
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : "Lançar pagamento"}
            </Button>
          </div>
        </form>
      )}

      {erroAcao && <p className="mb-3 text-sm text-red-600">{erroAcao}</p>}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os pagamentos." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.data.length === 0 && (
        <EmptyState mensagem="Nenhum pagamento lançado ainda." />
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

function DespesasTab() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Despesa>(
    ["financeiro", "despesas"],
    "/financeiro/despesas",
    { page, limit }
  );
  const { data: veiculos } = usePaginatedQuery<Veiculo>(["veiculos", "select"], "/veiculos", {
    page: 1,
    limit: 100,
  });

  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<DespesaFormInput, unknown, DespesaFormValues>({
    resolver: zodResolver(despesaSchema),
  });

  const registrarDespesa = useMutation({
    mutationFn: (valores: DespesaFormValues) =>
      apiClient.post("/financeiro/despesas", {
        ...valores,
        veiculo_id: valores.veiculo_id || null,
        data: `${valores.data}T00:00:00Z`,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["financeiro", "despesas"] });
      reset();
      setMostrarForm(false);
      setErroForm(null);
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const columnHelper = createColumnHelper<Despesa>();
  const placaVeiculo = (id: string | null) => veiculos?.data.find((v) => v.id === id)?.placa ?? "—";
  const columns = [
    columnHelper.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
    columnHelper.accessor("categoria", { header: "Categoria" }),
    columnHelper.accessor("veiculo_id", { header: "Veículo", cell: (info) => placaVeiculo(info.getValue()) }),
    columnHelper.accessor("valor", { header: "Valor", cell: (info) => formatarMoeda(info.getValue()) }),
  ];

  const podeLancar = hasPermission("financeiro:lancar");

  return (
    <div>
      {podeLancar && (
        <div className="mb-4">
          <Button onClick={() => setMostrarForm((v) => !v)}>
            {mostrarForm ? "Cancelar" : "Registrar despesa"}
          </Button>
        </div>
      )}

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) => registrarDespesa.mutate(valores))}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Categoria</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("categoria")}
            />
            {errors.categoria && <p className="text-xs text-red-600">{errors.categoria.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Veículo (opcional)</label>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("veiculo_id")}
            >
              <option value="">Nenhum</option>
              {veiculos?.data.map((veiculo) => (
                <option key={veiculo.id} value={veiculo.id}>
                  {veiculo.placa}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Valor</label>
            <input
              type="number"
              step="0.01"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("valor")}
            />
            {errors.valor && <p className="text-xs text-red-600">{errors.valor.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Data</label>
            <input
              type="date"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("data")}
            />
            {errors.data && <p className="text-xs text-red-600">{errors.data.message}</p>}
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : "Registrar despesa"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar as despesas." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.data.length === 0 && (
        <EmptyState mensagem="Nenhuma despesa registrada ainda." />
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

function RentabilidadeTab() {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["financeiro", "rentabilidade"],
    queryFn: async () =>
      (await apiClient.get<RentabilidadeVeiculo[]>("/financeiro/rentabilidade")).data,
  });

  if (isLoading) return <LoadingState />;
  if (isError) {
    return (
      <ErrorState mensagem="Não foi possível carregar a rentabilidade." aoTentarNovamente={() => refetch()} />
    );
  }
  if (!data || data.length === 0) {
    return <EmptyState mensagem="Sem dados de rentabilidade ainda." />;
  }

  return <RentabilidadeChart dados={data} />;
}
