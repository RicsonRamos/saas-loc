import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
import { useState } from "react";
import { useForm } from "react-hook-form";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient, extrairMensagemErro } from "@/core/api/client";
import { useAuth } from "@/core/auth/AuthContext";
import { formatarData } from "@/core/format";

import { leituraKmSchema, type LeituraKmFormInput, type LeituraKmFormValues } from "./leituraKmSchema";
import type { LeituraKm } from "./leituraKmTypes";

const columnHelper = createColumnHelper<LeituraKm>();

const CAMPOS_VAZIOS: LeituraKmFormInput = {
  data_leitura: "",
  km: 0,
  observacao: "",
};

export function LeiturasKmSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["leituras-km", { veiculo_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: LeituraKm[] }>("/leituras-km", {
          params: { veiculo_id: veiculoId, limit: 100 },
        })
      ).data.data,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<LeituraKmFormInput, unknown, LeituraKmFormValues>({
    resolver: zodResolver(leituraKmSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  const registrar = useMutation({
    mutationFn: (valores: LeituraKmFormValues) =>
      apiClient.post("/leituras-km", {
        veiculo_id: veiculoId,
        km: valores.km,
        data_leitura: `${valores.data_leitura}T00:00:00Z`,
        observacao: valores.observacao ?? null,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["leituras-km", { veiculo_id: veiculoId }] });
      void queryClient.invalidateQueries({ queryKey: ["veiculos", veiculoId] });
      void queryClient.invalidateQueries({ queryKey: ["veiculos", veiculoId, "historico"] });
      reset(CAMPOS_VAZIOS);
      setMostrarForm(false);
      setErroForm(null);
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const podeRegistrar = hasPermission("leituras_km:registrar");

  const dadosGrafico = [...(data ?? [])]
    .sort((a, b) => new Date(a.data_leitura).getTime() - new Date(b.data_leitura).getTime())
    .map((leitura) => ({ data: formatarData(leitura.data_leitura), km: leitura.km }));

  const columns = [
    columnHelper.accessor("data_leitura", {
      header: "Data",
      cell: (info) => formatarData(info.getValue()),
    }),
    columnHelper.accessor("km", { header: "KM" }),
    columnHelper.accessor("observacao", {
      header: "Observação",
      cell: (info) => info.getValue() ?? "—",
    }),
  ];

  return (
    <section>
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          Atualização de quilometragem
        </h2>
        {podeRegistrar && (
          <Button variante="secundaria" onClick={() => setMostrarForm((v) => !v)}>
            {mostrarForm ? "Cancelar" : "Registrar leitura"}
          </Button>
        )}
      </div>

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) => registrar.mutate(valores))}
          className="mb-4 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-3"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Data</label>
            <input
              type="date"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("data_leitura")}
            />
            {errors.data_leitura && (
              <p className="text-xs text-red-600">{errors.data_leitura.message}</p>
            )}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Quilometragem
            </label>
            <input
              type="number"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("km")}
            />
            {errors.km && <p className="text-xs text-red-600">{errors.km.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Observação (opcional)
            </label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("observacao")}
            />
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
          mensagem="Não foi possível carregar o histórico de quilometragem."
          aoTentarNovamente={() => refetch()}
        />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhuma leitura de quilometragem registrada para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <div className="flex flex-col gap-4">
          <div className="h-64 rounded-lg border border-slate-200 bg-white p-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dadosGrafico}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="data" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip formatter={(valor) => `${valor} km`} />
                <Line type="monotone" dataKey="km" stroke="#0f172a" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <DataTable columns={columns} data={data} />
        </div>
      )}
    </section>
  );
}
