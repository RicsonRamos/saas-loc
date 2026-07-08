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
import { formatarData, formatarMoeda } from "@/core/format";
import { usePaginatedQuery } from "@/core/hooks/usePaginatedQuery";
import type { Veiculo } from "@/features/frota/types";

import { manutencaoSchema, type ManutencaoFormInput, type ManutencaoFormValues } from "./schema";
import type { Manutencao } from "./types";

const columnHelper = createColumnHelper<Manutencao>();

const columns = [
  columnHelper.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
  columnHelper.accessor("tipo", {
    header: "Tipo",
    cell: (info) => (info.getValue() === "preventiva" ? "Preventiva" : "Corretiva"),
  }),
  columnHelper.accessor("km", { header: "KM" }),
  columnHelper.accessor("custo", { header: "Custo", cell: (info) => formatarMoeda(info.getValue()) }),
  columnHelper.accessor("oficina", { header: "Oficina", cell: (info) => info.getValue() ?? "—" }),
];

export function ManutencoesPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const limit = 20;

  const { data, isLoading, isError, refetch } = usePaginatedQuery<Manutencao>(
    ["manutencoes"],
    "/manutencoes",
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
  } = useForm<ManutencaoFormInput, unknown, ManutencaoFormValues>({
    resolver: zodResolver(manutencaoSchema),
    defaultValues: { tipo: "preventiva", em_andamento: false },
  });

  const registrarManutencao = useMutation({
    mutationFn: (valores: ManutencaoFormValues) =>
      apiClient.post("/manutencoes", { ...valores, data: `${valores.data}T00:00:00Z` }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["manutencoes"] });
      void queryClient.invalidateQueries({ queryKey: ["veiculos"] });
      reset();
      setMostrarForm(false);
      setErroForm(null);
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const podeRegistrar = hasPermission("manutencoes:registrar");

  return (
    <div>
      <PageHeader
        title="Manutenções"
        actions={
          podeRegistrar && (
            <Button onClick={() => setMostrarForm((v) => !v)}>
              {mostrarForm ? "Cancelar" : "Registrar manutenção"}
            </Button>
          )
        }
      />

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) => registrarManutencao.mutate(valores))}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Veículo</label>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("veiculo_id")}
            >
              <option value="">Selecione...</option>
              {veiculos?.data.map((veiculo) => (
                <option key={veiculo.id} value={veiculo.id}>
                  {veiculo.placa} — {veiculo.modelo}
                </option>
              ))}
            </select>
            {errors.veiculo_id && <p className="text-xs text-red-600">{errors.veiculo_id.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Tipo</label>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("tipo")}
            >
              <option value="preventiva">Preventiva</option>
              <option value="corretiva">Corretiva</option>
            </select>
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
            <label className="mb-1 block text-sm font-medium text-slate-700">KM</label>
            <input
              type="number"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("km")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Custo</label>
            <input
              type="number"
              step="0.01"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("custo")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Oficina</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("oficina")}
            />
          </div>
          <div className="flex items-end gap-2">
            <input type="checkbox" id="em_andamento" {...register("em_andamento")} />
            <label htmlFor="em_andamento" className="text-sm text-slate-700">
              Veículo fica em manutenção agora
            </label>
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : "Registrar"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState
          mensagem="Não foi possível carregar as manutenções."
          aoTentarNovamente={() => refetch()}
        />
      )}
      {!isLoading && !isError && data && data.data.length === 0 && (
        <EmptyState mensagem="Nenhuma manutenção registrada ainda." />
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
