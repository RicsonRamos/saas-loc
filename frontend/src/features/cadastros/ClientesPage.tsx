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
import { usePaginatedQuery } from "@/core/hooks/usePaginatedQuery";

import { clienteSchema, type ClienteFormValues } from "./schema";
import type { Cliente } from "./types";

const columnHelper = createColumnHelper<Cliente>();

export function ClientesPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Cliente>(
    ["clientes"],
    "/clientes",
    { page, limit }
  );

  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ClienteFormValues>({ resolver: zodResolver(clienteSchema) });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["clientes"] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset({ nome: "", documento: "", email: "", telefone: "" });
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(cliente: Cliente) {
    setEditandoId(cliente.id);
    reset({
      nome: cliente.nome,
      documento: cliente.documento,
      email: cliente.email ?? "",
      telefone: cliente.telefone ?? "",
    });
    setErroForm(null);
    setMostrarForm(true);
  }

  function fecharForm() {
    setMostrarForm(false);
    setEditandoId(null);
    reset({ nome: "", documento: "", email: "", telefone: "" });
    setErroForm(null);
  }

  const criarCliente = useMutation({
    mutationFn: (valores: ClienteFormValues) => apiClient.post("/clientes", valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizarCliente = useMutation({
    mutationFn: (valores: ClienteFormValues) =>
      apiClient.patch(`/clientes/${editandoId}`, {
        nome: valores.nome,
        email: valores.email,
        telefone: valores.telefone,
      }),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const removerCliente = useMutation({
    mutationFn: (clienteId: string) => apiClient.delete(`/clientes/${clienteId}`),
    onSuccess: () => {
      invalidar();
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  function excluir(cliente: Cliente) {
    if (window.confirm(`Excluir o cliente ${cliente.nome}?`)) {
      removerCliente.mutate(cliente.id);
    }
  }

  const podeEditar = hasPermission("clientes:editar");

  const columns = [
    columnHelper.accessor("nome", { header: "Nome" }),
    columnHelper.accessor("documento", { header: "Documento" }),
    columnHelper.accessor("email", { header: "E-mail", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("telefone", {
      header: "Telefone",
      cell: (info) => info.getValue() ?? "—",
    }),
    ...(podeEditar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Cliente } }) => {
              const cliente = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(cliente)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(cliente)}
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
        title="Clientes"
        actions={
          podeEditar && (
            <Button onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}>
              {mostrarForm ? "Cancelar" : "Novo cliente"}
            </Button>
          )
        }
      />

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) =>
            editandoId ? atualizarCliente.mutate(valores) : criarCliente.mutate(valores)
          )}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Nome</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("nome")} />
            {errors.nome && <p className="text-xs text-red-600">{errors.nome.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Documento</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm disabled:bg-slate-100"
              disabled={!!editandoId}
              {...register("documento")}
            />
            {errors.documento && <p className="text-xs text-red-600">{errors.documento.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">E-mail</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("email")} />
            {errors.email && <p className="text-xs text-red-600">{errors.email.message}</p>}
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
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar cliente" : "Salvar cliente"}
            </Button>
          </div>
        </form>
      )}

      {erroAcao && <p className="mb-3 text-sm text-red-600">{erroAcao}</p>}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os clientes." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.data.length === 0 && (
        <EmptyState mensagem="Nenhum cliente cadastrado ainda." />
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
