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
import { formatarData } from "@/core/format";
import { usePaginatedQuery } from "@/core/hooks/usePaginatedQuery";

import { motoristaSchema, type MotoristaFormValues } from "./schema";
import type { Motorista } from "./types";

const columnHelper = createColumnHelper<Motorista>();

const columns = [
  columnHelper.accessor("nome", { header: "Nome" }),
  columnHelper.accessor("cnh", { header: "CNH" }),
  columnHelper.accessor("validade_cnh", {
    header: "Validade da CNH",
    cell: (info) => formatarData(info.getValue()),
  }),
  columnHelper.accessor("telefone", { header: "Telefone", cell: (info) => info.getValue() ?? "—" }),
];

export function MotoristasPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Motorista>(
    ["motoristas"],
    "/motoristas",
    { page, limit }
  );

  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<MotoristaFormValues>({ resolver: zodResolver(motoristaSchema) });

  const criarMotorista = useMutation({
    mutationFn: (valores: MotoristaFormValues) => apiClient.post("/motoristas", valores),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["motoristas"] });
      reset();
      setMostrarForm(false);
      setErroForm(null);
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const podeEditar = hasPermission("motoristas:editar");

  return (
    <div>
      <PageHeader
        title="Motoristas"
        actions={
          podeEditar && (
            <Button onClick={() => setMostrarForm((v) => !v)}>
              {mostrarForm ? "Cancelar" : "Novo motorista"}
            </Button>
          )
        }
      />

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) => criarMotorista.mutate(valores))}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Nome</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("nome")} />
            {errors.nome && <p className="text-xs text-red-600">{errors.nome.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">CNH</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("cnh")} />
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
              {isSubmitting ? "Salvando..." : "Salvar motorista"}
            </Button>
          </div>
        </form>
      )}

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
