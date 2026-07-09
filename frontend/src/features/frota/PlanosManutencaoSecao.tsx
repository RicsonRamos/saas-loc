import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createColumnHelper } from "@tanstack/react-table";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/Button";
import { DataTable } from "@/components/ui/DataTable";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient, extrairMensagemErro } from "@/core/api/client";
import { useAuth } from "@/core/auth/AuthContext";

import {
  planoManutencaoSchema,
  type PlanoManutencaoFormInput,
  type PlanoManutencaoFormValues,
} from "./planoManutencaoSchema";
import type { PlanoManutencao, PrioridadePlano } from "./planoManutencaoTypes";

const columnHelper = createColumnHelper<PlanoManutencao>();

const ROTULOS_TIPO: Record<string, string> = {
  troca_oleo: "Troca de óleo",
  troca_filtros: "Troca de filtros",
  pastilhas_freio: "Pastilhas de freio",
  pneus: "Pneus",
  revisao: "Revisão periódica",
  alinhamento_balanceamento: "Alinhamento e balanceamento",
  licenciamento: "Licenciamento",
  seguro: "Seguro",
  outro: "Outro",
};

const ESTILO_POR_PRIORIDADE: Record<PrioridadePlano, string> = {
  normal: "bg-slate-100 text-slate-700",
  atencao: "bg-amber-100 text-amber-800",
  critico: "bg-red-100 text-red-800",
};

const CAMPOS_VAZIOS: PlanoManutencaoFormInput = {
  tipo: "troca_oleo",
  descricao: "",
  intervalo_km: "",
  intervalo_dias: "",
  ultima_execucao_km: "",
  ultima_execucao_data: "",
};

export function PlanosManutencaoSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["planos-manutencao", { veiculo_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: PlanoManutencao[] }>("/planos-manutencao", {
          params: { veiculo_id: veiculoId, limit: 100 },
        })
      ).data.data,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<PlanoManutencaoFormInput, unknown, PlanoManutencaoFormValues>({
    resolver: zodResolver(planoManutencaoSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({
      queryKey: ["planos-manutencao", { veiculo_id: veiculoId }],
    });
    void queryClient.invalidateQueries({ queryKey: ["dashboard", "resumo"] });
  }

  const criar = useMutation({
    mutationFn: (valores: PlanoManutencaoFormValues) =>
      apiClient.post("/planos-manutencao", {
        veiculo_id: veiculoId,
        tipo: valores.tipo,
        descricao: valores.descricao ?? null,
        intervalo_km: valores.intervalo_km ?? null,
        intervalo_dias: valores.intervalo_dias ?? null,
        ultima_execucao_km: valores.ultima_execucao_km ?? null,
        ultima_execucao_data: valores.ultima_execucao_data ?? null,
      }),
    onSuccess: () => {
      invalidar();
      reset(CAMPOS_VAZIOS);
      setMostrarForm(false);
      setErroForm(null);
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const remover = useMutation({
    mutationFn: (id: string) => apiClient.delete(`/planos-manutencao/${id}`),
    onSuccess: () => invalidar(),
  });

  function excluir(plano: PlanoManutencao) {
    if (window.confirm(`Remover o plano de ${ROTULOS_TIPO[plano.tipo] ?? plano.tipo}?`)) {
      remover.mutate(plano.id);
    }
  }

  const podeRegistrar = hasPermission("manutencoes:registrar");

  const columns = [
    columnHelper.accessor("tipo", {
      header: "Tipo",
      cell: (info) => info.row.original.descricao || ROTULOS_TIPO[info.getValue()] || info.getValue(),
    }),
    columnHelper.accessor("intervalo_km", {
      header: "Intervalo (km)",
      cell: (info) => info.getValue() ?? "—",
    }),
    columnHelper.accessor("intervalo_dias", {
      header: "Intervalo (dias)",
      cell: (info) => info.getValue() ?? "—",
    }),
    columnHelper.display({
      id: "faltam",
      header: "Faltam",
      cell: (info) => {
        const { faltam_km, faltam_dias } = info.row.original;
        const partes: string[] = [];
        if (faltam_km !== null) partes.push(`${faltam_km} km`);
        if (faltam_dias !== null) partes.push(`${faltam_dias} dias`);
        return partes.length > 0 ? partes.join(" / ") : "—";
      },
    }),
    columnHelper.accessor("prioridade", {
      header: "Prioridade",
      cell: (info) => (
        <span
          className={`rounded-full px-2 py-1 text-xs font-medium ${ESTILO_POR_PRIORIDADE[info.getValue()]}`}
        >
          {info.getValue()}
        </span>
      ),
    }),
    ...(podeRegistrar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: PlanoManutencao } }) => (
              <button
                className="text-xs text-red-700 underline"
                onClick={() => excluir(info.row.original)}
              >
                Excluir
              </button>
            ),
          }),
        ]
      : []),
  ];

  return (
    <section>
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          Planos de manutenção preventiva
        </h2>
        {podeRegistrar && (
          <Button variante="secundaria" onClick={() => setMostrarForm((v) => !v)}>
            {mostrarForm ? "Cancelar" : "Novo plano"}
          </Button>
        )}
      </div>

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) => criar.mutate(valores))}
          className="mb-4 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-3"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Tipo</label>
            <select
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("tipo")}
            >
              {Object.entries(ROTULOS_TIPO).map(([valor, rotulo]) => (
                <option key={valor} value={valor}>
                  {rotulo}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Descrição (para "Outro")
            </label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("descricao")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Intervalo (km)
            </label>
            <input
              type="number"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("intervalo_km")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Intervalo (dias)
            </label>
            <input
              type="number"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("intervalo_dias")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Última execução (km)
            </label>
            <input
              type="number"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("ultima_execucao_km")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Última execução (data)
            </label>
            <input
              type="date"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("ultima_execucao_data")}
            />
          </div>
          {errors.intervalo_km && (
            <p className="col-span-full text-xs text-red-600">{errors.intervalo_km.message}</p>
          )}
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : "Criar plano"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState
          mensagem="Não foi possível carregar os planos de manutenção."
          aoTentarNovamente={() => refetch()}
        />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhum plano de manutenção configurado para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <DataTable columns={columns} data={data} />
      )}
    </section>
  );
}
