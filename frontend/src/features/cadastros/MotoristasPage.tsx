import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
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
import { formatarData } from "@/core/format";
import { usePaginatedQuery } from "@/core/hooks/usePaginatedQuery";

import { motoristaSchema, type MotoristaFormValues } from "./schema";
import type { Cliente, Motorista } from "./types";

const columnHelper = createColumnHelper<Motorista>();

export function MotoristasPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Motorista>(
    ["motoristas"],
    "/motoristas",
    { page, limit }
  );
  const { data: clientes } = usePaginatedQuery<Cliente>(["clientes", "select"], "/clientes", {
    page: 1,
    limit: 100,
  });

  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<MotoristaFormValues>({ resolver: zodResolver(motoristaSchema) });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["motoristas"] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset({ nome: "", cnh: "", validade_cnh: "", telefone: "" });
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(motorista: Motorista) {
    setEditandoId(motorista.id);
    reset({
      nome: motorista.nome,
      cnh: motorista.cnh,
      validade_cnh: motorista.validade_cnh,
      telefone: motorista.telefone ?? "",
    });
    setErroForm(null);
    setMostrarForm(true);
  }

  function fecharForm() {
    setMostrarForm(false);
    setEditandoId(null);
    reset({ nome: "", cnh: "", validade_cnh: "", telefone: "" });
    setErroForm(null);
  }

  const criarMotorista = useMutation({
    mutationFn: (valores: MotoristaFormValues) => apiClient.post("/motoristas", valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizarMotorista = useMutation({
    mutationFn: (valores: MotoristaFormValues) =>
      apiClient.patch(`/motoristas/${editandoId}`, {
        nome: valores.nome,
        validade_cnh: valores.validade_cnh,
        telefone: valores.telefone,
      }),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const removerMotorista = useMutation({
    mutationFn: (motoristaId: string) => apiClient.delete(`/motoristas/${motoristaId}`),
    onSuccess: () => {
      invalidar();
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  function excluir(motorista: Motorista) {
    if (window.confirm(`Excluir o motorista ${motorista.nome}?`)) {
      removerMotorista.mutate(motorista.id);
    }
  }

  const podeEditar = hasPermission("motoristas:editar");

  const columns = [
    columnHelper.accessor("nome", { header: "Nome" }),
    columnHelper.accessor("cnh", { header: "CNH" }),
    columnHelper.accessor("validade_cnh", {
      header: "Validade da CNH",
      cell: (info) => formatarData(info.getValue()),
    }),
    columnHelper.accessor("telefone", {
      header: "Telefone",
      cell: (info) => info.getValue() ?? "—",
    }),
    columnHelper.accessor("cliente_id", {
      header: "Cliente vinculado",
      cell: (info) => {
        const clienteId = info.getValue();
        if (!clienteId) return "—";
        const cliente = clientes?.data.find((c) => c.id === clienteId);
        return (
          <Link className="underline" to={`/clientes/${clienteId}`}>
            {cliente?.nome ?? "Ver cliente"}
          </Link>
        );
      },
    }),
    ...(podeEditar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Motorista } }) => {
              const motorista = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(motorista)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(motorista)}
                  >
                    Excluir
                  </button>
                </div>
              );
            },
          }),
        ]
      : []),
  ];

  return (
    <div>
      <PageHeader
        title="Motoristas"
        actions={
          podeEditar && (
            <Button onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}>
              {mostrarForm ? "Cancelar" : "Novo motorista"}
            </Button>
          )
        }
      />

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) =>
            editandoId ? atualizarMotorista.mutate(valores) : criarMotorista.mutate(valores)
          )}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Nome</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("nome")} />
            {errors.nome && <p className="text-xs text-red-600">{errors.nome.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">CNH</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm disabled:bg-slate-100"
              disabled={!!editandoId}
              {...register("cnh")}
            />
            {errors.cnh && <p className="text-xs text-red-600">{errors.cnh.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Validade da CNH</label>
            <input
              type="date"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("validade_cnh")}
            />
            {errors.validade_cnh && (
              <p className="text-xs text-red-600">{errors.validade_cnh.message}</p>
            )}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Telefone</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("telefone")}
            />
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar motorista" : "Salvar motorista"}
            </Button>
          </div>
        </form>
      )}

      {erroAcao && <p className="mb-3 text-sm text-red-600">{erroAcao}</p>}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState
          mensagem="Não foi possível carregar os motoristas."
          aoTentarNovamente={() => refetch()}
        />
      )}
      {!isLoading && !isError && data && data.data.length === 0 && (
        <EmptyState mensagem="Nenhum motorista cadastrado ainda." />
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
