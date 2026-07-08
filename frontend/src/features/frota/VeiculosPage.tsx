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

import { veiculoSchema, type VeiculoFormInput, type VeiculoFormValues } from "./schema";
import { StatusVeiculoBadge } from "./StatusVeiculoBadge";
import type { Veiculo } from "./types";

const columnHelper = createColumnHelper<Veiculo>();

const columns = [
  columnHelper.accessor("placa", { header: "Placa" }),
  columnHelper.accessor("modelo", { header: "Modelo" }),
  columnHelper.accessor("ano", { header: "Ano" }),
  columnHelper.accessor("km_atual", { header: "KM atual" }),
  columnHelper.accessor("status", {
    header: "Status",
    cell: (info) => <StatusVeiculoBadge status={info.getValue()} />,
  }),
];

export function VeiculosPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Veiculo>(
    ["veiculos"],
    "/veiculos",
    { page, limit }
  );

  const queryClient = useQueryClient();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<VeiculoFormInput, unknown, VeiculoFormValues>({
    resolver: zodResolver(veiculoSchema),
    defaultValues: { km_atual: 0 },
  });

  const criarVeiculo = useMutation({
    mutationFn: (valores: VeiculoFormValues) => apiClient.post("/veiculos", valores),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["veiculos"] });
      reset();
      setMostrarForm(false);
      setErroForm(null);
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const podeEditar = hasPermission("frota:editar");

  return (
    <div>
      <PageHeader
        title="Frota"
        actions={
          podeEditar && (
            <Button onClick={() => setMostrarForm((v) => !v)}>
              {mostrarForm ? "Cancelar" : "Novo veículo"}
            </Button>
          )
        }
      />

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) => criarVeiculo.mutate(valores))}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Placa</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("placa")}
            />
            {errors.placa && <p className="text-xs text-red-600">{errors.placa.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Modelo</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("modelo")}
            />
            {errors.modelo && <p className="text-xs text-red-600">{errors.modelo.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Ano</label>
            <input
              type="number"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("ano")}
            />
            {errors.ano && <p className="text-xs text-red-600">{errors.ano.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">KM atual</label>
            <input
              type="number"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("km_atual")}
            />
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : "Salvar veículo"}
            </Button>
          </div>
        </form>
      )}

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
