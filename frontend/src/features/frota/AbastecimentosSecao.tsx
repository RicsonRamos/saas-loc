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
import { formatarData, formatarMoeda } from "@/core/format";

import {
  abastecimentoSchema,
  type AbastecimentoFormInput,
  type AbastecimentoFormValues,
} from "./abastecimentoPneuSchema";
import type { Abastecimento } from "./abastecimentoPneuTypes";

const columnHelper = createColumnHelper<Abastecimento>();

const CAMPOS_VAZIOS: AbastecimentoFormInput = {
  data: "",
  posto: "",
  litros: "",
  valor: "",
  km: 0,
  tipo_combustivel: "",
};

export function AbastecimentosSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["abastecimentos", { veiculo_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: Abastecimento[] }>("/abastecimentos", {
          params: { veiculo_id: veiculoId, limit: 100 },
        })
      ).data.data,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<AbastecimentoFormInput, unknown, AbastecimentoFormValues>({
    resolver: zodResolver(abastecimentoSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({
      queryKey: ["abastecimentos", { veiculo_id: veiculoId }],
    });
    void queryClient.invalidateQueries({ queryKey: ["veiculos", veiculoId, "historico"] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(abastecimento: Abastecimento) {
    setEditandoId(abastecimento.id);
    reset({
      data: abastecimento.data.slice(0, 10),
      posto: abastecimento.posto ?? "",
      litros: abastecimento.litros,
      valor: abastecimento.valor,
      km: abastecimento.km,
      tipo_combustivel: abastecimento.tipo_combustivel ?? "",
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

  const criar = useMutation({
    mutationFn: (valores: AbastecimentoFormValues) =>
      apiClient.post("/abastecimentos", {
        ...valores,
        veiculo_id: veiculoId,
        data: `${valores.data}T00:00:00Z`,
      }),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizar = useMutation({
    mutationFn: (valores: AbastecimentoFormValues) =>
      apiClient.patch(`/abastecimentos/${editandoId}`, {
        ...valores,
        data: `${valores.data}T00:00:00Z`,
      }),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const remover = useMutation({
    mutationFn: (id: string) => apiClient.delete(`/abastecimentos/${id}`),
    onSuccess: () => invalidar(),
  });

  function excluir(abastecimento: Abastecimento) {
    if (window.confirm(`Excluir este abastecimento de ${formatarData(abastecimento.data)}?`)) {
      remover.mutate(abastecimento.id);
    }
  }

  const podeRegistrar = hasPermission("abastecimentos:registrar");

  const columns = [
    columnHelper.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
    columnHelper.accessor("posto", { header: "Posto", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("litros", { header: "Litros" }),
    columnHelper.accessor("valor", { header: "Valor", cell: (info) => formatarMoeda(info.getValue()) }),
    columnHelper.accessor("valor_por_litro", {
      header: "Valor/litro",
      cell: (info) => formatarMoeda(info.getValue()),
    }),
    columnHelper.accessor("km", { header: "KM" }),
    columnHelper.accessor("tipo_combustivel", {
      header: "Combustível",
      cell: (info) => info.getValue() ?? "—",
    }),
    ...(podeRegistrar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Abastecimento } }) => {
              const abastecimento = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(abastecimento)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(abastecimento)}
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
    <section>
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
          Abastecimentos
        </h2>
        {podeRegistrar && (
          <Button
            variante="secundaria"
            onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}
          >
            {mostrarForm ? "Cancelar" : "Registrar abastecimento"}
          </Button>
        )}
      </div>

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) =>
            editandoId ? atualizar.mutate(valores) : criar.mutate(valores)
          )}
          className="mb-4 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Data</label>
            <input type="date" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("data")} />
            {errors.data && <p className="text-xs text-red-600">{errors.data.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Posto</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("posto")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Litros</label>
            <input type="number" step="0.001" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("litros")} />
            {errors.litros && <p className="text-xs text-red-600">{errors.litros.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Valor</label>
            <input type="number" step="0.01" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("valor")} />
            {errors.valor && <p className="text-xs text-red-600">{errors.valor.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">KM</label>
            <input type="number" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("km")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Combustível</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              placeholder="Ex.: Gasolina, Etanol, Diesel"
              {...register("tipo_combustivel")}
            />
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar" : "Registrar"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os abastecimentos." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhum abastecimento registrado para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <DataTable columns={columns} data={data} />
      )}
    </section>
  );
}
