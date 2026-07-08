import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
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
import { formatarDataHora, formatarMoeda } from "@/core/format";
import { usePaginatedQuery } from "@/core/hooks/usePaginatedQuery";
import type { Cliente } from "@/features/cadastros/types";
import type { Veiculo } from "@/features/frota/types";

import { ChecklistComparacao } from "@/features/checklists/ChecklistComparacao";
import { ChecklistForm } from "@/features/checklists/ChecklistForm";
import type { TipoChecklist } from "@/features/checklists/checklistTypes";

import { contratoSchema, type ContratoFormInput, type ContratoFormValues } from "./schema";
import { StatusContratoBadge } from "./StatusContratoBadge";
import type { Contrato } from "./types";

function paraIsoUtc(dataLocal: string): string {
  return new Date(dataLocal).toISOString();
}

export function ContratosPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  const [checklistAberto, setChecklistAberto] = useState<{
    contratoId: string;
    tipo: TipoChecklist;
  } | null>(null);
  const [comparacaoContratoId, setComparacaoContratoId] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Contrato>(
    ["contratos"],
    "/contratos",
    { page, limit }
  );
  const { data: clientes } = usePaginatedQuery<Cliente>(["clientes", "select"], "/clientes", {
    page: 1,
    limit: 100,
  });
  const { data: veiculosDisponiveis } = usePaginatedQuery<Veiculo>(
    ["veiculos", "select"],
    "/veiculos",
    { page: 1, limit: 100 }
  );
  const queryClient = useQueryClient();

  function invalidarTudo() {
    void queryClient.invalidateQueries({ queryKey: ["contratos"] });
    void queryClient.invalidateQueries({ queryKey: ["veiculos"] });
  }

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ContratoFormInput, unknown, ContratoFormValues>({ resolver: zodResolver(contratoSchema) });

  const criarContrato = useMutation({
    mutationFn: (valores: ContratoFormValues) =>
      apiClient.post("/contratos", {
        cliente_id: valores.cliente_id,
        veiculo_id: valores.veiculo_id,
        data_inicio: paraIsoUtc(valores.data_inicio),
        data_fim_prevista: paraIsoUtc(valores.data_fim_prevista),
        valor_diaria: valores.valor_diaria,
      }),
    onSuccess: () => {
      invalidarTudo();
      reset();
      setMostrarForm(false);
      setErroForm(null);
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const devolverContrato = useMutation({
    mutationFn: (contratoId: string) => apiClient.patch(`/contratos/${contratoId}/devolucao`, {}),
    onSuccess: () => {
      invalidarTudo();
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  const cancelarContrato = useMutation({
    mutationFn: (contratoId: string) => apiClient.patch(`/contratos/${contratoId}/cancelamento`),
    onSuccess: () => {
      invalidarTudo();
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  const columnHelper = createColumnHelper<Contrato>();
  const nomeCliente = (id: string) => clientes?.data.find((c) => c.id === id)?.nome ?? id;
  const placaVeiculo = (id: string) => veiculosDisponiveis?.data.find((v) => v.id === id)?.placa ?? id;

  const columns = [
    columnHelper.accessor("cliente_id", { header: "Cliente", cell: (info) => nomeCliente(info.getValue()) }),
    columnHelper.accessor("veiculo_id", { header: "Veículo", cell: (info) => placaVeiculo(info.getValue()) }),
    columnHelper.accessor("data_inicio", {
      header: "Início",
      cell: (info) => formatarDataHora(info.getValue()),
    }),
    columnHelper.accessor("data_fim_prevista", {
      header: "Devolução prevista",
      cell: (info) => formatarDataHora(info.getValue()),
    }),
    columnHelper.accessor("valor_diaria", {
      header: "Diária",
      cell: (info) => formatarMoeda(info.getValue()),
    }),
    columnHelper.accessor("status", { header: "Status", cell: (info) => <StatusContratoBadge status={info.getValue()} /> }),
    columnHelper.display({
      id: "acoes",
      header: "Ações",
      cell: (info) => {
        const contrato = info.row.original;
        const podeRegistrarChecklist = contrato.status === "ativo" && hasPermission("checklists:registrar");
        const podeVerComparacao = hasPermission("checklists:visualizar");
        return (
          <div className="flex flex-wrap gap-2">
            {contrato.status === "ativo" && hasPermission("contratos:emitir") && (
              <>
                <button
                  className="text-xs text-blue-700 underline"
                  onClick={() => devolverContrato.mutate(contrato.id)}
                >
                  Devolver
                </button>
                <button
                  className="text-xs text-red-700 underline"
                  onClick={() => cancelarContrato.mutate(contrato.id)}
                >
                  Cancelar
                </button>
              </>
            )}
            {podeRegistrarChecklist && (
              <>
                <button
                  className="text-xs text-slate-700 underline"
                  onClick={() =>
                    setChecklistAberto({ contratoId: contrato.id, tipo: "entrega" })
                  }
                >
                  Checklist entrega
                </button>
                <button
                  className="text-xs text-slate-700 underline"
                  onClick={() =>
                    setChecklistAberto({ contratoId: contrato.id, tipo: "devolucao" })
                  }
                >
                  Checklist devolução
                </button>
              </>
            )}
            {podeVerComparacao && (
              <button
                className="text-xs text-slate-700 underline"
                onClick={() =>
                  setComparacaoContratoId(
                    comparacaoContratoId === contrato.id ? null : contrato.id
                  )
                }
              >
                {comparacaoContratoId === contrato.id ? "Ocultar comparação" : "Comparar"}
              </button>
            )}
          </div>
        );
      },
    }),
  ];

  const podeEmitir = hasPermission("contratos:emitir");

  return (
    <div>
      <PageHeader
        title="Contratos"
        actions={
          podeEmitir && (
            <Button onClick={() => setMostrarForm((v) => !v)}>
              {mostrarForm ? "Cancelar" : "Nova locação"}
            </Button>
          )
        }
      />

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) => criarContrato.mutate(valores))}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-3"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Cliente</label>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("cliente_id")}
            >
              <option value="">Selecione...</option>
              {clientes?.data.map((cliente) => (
                <option key={cliente.id} value={cliente.id}>
                  {cliente.nome}
                </option>
              ))}
            </select>
            {errors.cliente_id && <p className="text-xs text-red-600">{errors.cliente_id.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Veículo</label>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("veiculo_id")}
            >
              <option value="">Selecione...</option>
              {veiculosDisponiveis?.data
                .filter((v) => v.status === "disponivel")
                .map((veiculo) => (
                  <option key={veiculo.id} value={veiculo.id}>
                    {veiculo.placa} — {veiculo.modelo}
                  </option>
                ))}
            </select>
            {errors.veiculo_id && <p className="text-xs text-red-600">{errors.veiculo_id.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Início</label>
            <input
              type="datetime-local"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("data_inicio")}
            />
            {errors.data_inicio && <p className="text-xs text-red-600">{errors.data_inicio.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Devolução prevista</label>
            <input
              type="datetime-local"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("data_fim_prevista")}
            />
            {errors.data_fim_prevista && (
              <p className="text-xs text-red-600">{errors.data_fim_prevista.message}</p>
            )}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Valor da diária</label>
            <input
              type="number"
              step="0.01"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("valor_diaria")}
            />
            {errors.valor_diaria && (
              <p className="text-xs text-red-600">{errors.valor_diaria.message}</p>
            )}
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : "Criar locação"}
            </Button>
          </div>
        </form>
      )}

      {erroAcao && <p className="mb-3 text-sm text-red-600">{erroAcao}</p>}

      {checklistAberto && (
        <ChecklistForm
          contratoId={checklistAberto.contratoId}
          tipo={checklistAberto.tipo}
          onCancelar={() => setChecklistAberto(null)}
          onConcluido={() => setChecklistAberto(null)}
        />
      )}

      {comparacaoContratoId && (
        <div className="mb-6">
          <ChecklistComparacao contratoId={comparacaoContratoId} />
        </div>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os contratos." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.data.length === 0 && (
        <EmptyState mensagem="Nenhum contrato registrado ainda." />
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
