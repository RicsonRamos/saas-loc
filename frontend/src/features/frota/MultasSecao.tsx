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

import { multaSchema, type MultaFormInput, type MultaFormValues } from "./incidentesSchema";
import type { Multa } from "./incidentesTypes";

const columnHelper = createColumnHelper<Multa>();

const CAMPOS_VAZIOS: MultaFormInput = {
  data: "",
  infracao: "",
  local: "",
  valor: "",
  pontos: "",
  status: "pendente",
  observacoes: "",
};

export function MultasSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["multas", { veiculo_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: Multa[] }>("/multas", {
          params: { veiculo_id: veiculoId, limit: 100 },
        })
      ).data.data,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<MultaFormInput, unknown, MultaFormValues>({
    resolver: zodResolver(multaSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["multas", { veiculo_id: veiculoId }] });
    void queryClient.invalidateQueries({ queryKey: ["dashboard", "resumo"] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(multa: Multa) {
    setEditandoId(multa.id);
    reset({
      data: multa.data.slice(0, 10),
      infracao: multa.infracao,
      local: multa.local ?? "",
      valor: multa.valor,
      pontos: multa.pontos != null ? String(multa.pontos) : "",
      status: multa.status,
      observacoes: multa.observacoes ?? "",
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
    mutationFn: (valores: MultaFormValues) =>
      apiClient.post("/multas", {
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
    mutationFn: (valores: MultaFormValues) =>
      apiClient.patch(`/multas/${editandoId}`, {
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
    mutationFn: (id: string) => apiClient.delete(`/multas/${id}`),
    onSuccess: () => invalidar(),
  });

  function excluir(multa: Multa) {
    if (window.confirm(`Excluir a multa "${multa.infracao}"?`)) {
      remover.mutate(multa.id);
    }
  }

  const podeRegistrar = hasPermission("multas:registrar");

  const columns = [
    columnHelper.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
    columnHelper.accessor("infracao", { header: "Infração" }),
    columnHelper.accessor("valor", { header: "Valor", cell: (info) => formatarMoeda(info.getValue()) }),
    columnHelper.accessor("pontos", { header: "Pontos", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("status", { header: "Situação" }),
    ...(podeRegistrar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Multa } }) => {
              const multa = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(multa)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(multa)}
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
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Multas</h2>
        {podeRegistrar && (
          <Button
            variante="secundaria"
            onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}
          >
            {mostrarForm ? "Cancelar" : "Registrar multa"}
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
          <div className="sm:col-span-2">
            <label className="mb-1 block text-sm font-medium text-slate-700">Infração</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("infracao")} />
            {errors.infracao && <p className="text-xs text-red-600">{errors.infracao.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Local</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("local")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Valor</label>
            <input type="number" step="0.01" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("valor")} />
            {errors.valor && <p className="text-xs text-red-600">{errors.valor.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Pontos</label>
            <input type="number" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("pontos")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Situação</label>
            <select className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("status")}>
              <option value="pendente">Pendente</option>
              <option value="paga">Paga</option>
              <option value="recorrida">Recorrida</option>
              <option value="cancelada">Cancelada</option>
            </select>
          </div>
          <div className="sm:col-span-2">
            <label className="mb-1 block text-sm font-medium text-slate-700">Observações</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("observacoes")} />
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar multa" : "Registrar multa"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar as multas." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhuma multa registrada para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <DataTable columns={columns} data={data} />
      )}
    </section>
  );
}
