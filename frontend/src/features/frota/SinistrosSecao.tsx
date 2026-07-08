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
import { formatarDataHora, formatarMoeda } from "@/core/format";

import { sinistroSchema, type SinistroFormInput, type SinistroFormValues } from "./incidentesSchema";
import type { Sinistro } from "./incidentesTypes";

const columnHelper = createColumnHelper<Sinistro>();

const CAMPOS_VAZIOS: SinistroFormInput = {
  tipo: "batida",
  data: "",
  descricao: "",
  valor_prejuizo: "",
  seguradora_acionada: false,
  status: "aberto",
};

const ROTULOS_TIPO: Record<string, string> = {
  batida: "Batida",
  roubo: "Roubo",
  furto: "Furto",
  enchente: "Enchente",
  incendio: "Incêndio",
};

export function SinistrosSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["sinistros", { veiculo_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: Sinistro[] }>("/sinistros", {
          params: { veiculo_id: veiculoId, limit: 100 },
        })
      ).data.data,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<SinistroFormInput, unknown, SinistroFormValues>({
    resolver: zodResolver(sinistroSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["sinistros", { veiculo_id: veiculoId }] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(sinistro: Sinistro) {
    setEditandoId(sinistro.id);
    reset({
      tipo: sinistro.tipo,
      data: sinistro.data.slice(0, 10),
      descricao: sinistro.descricao ?? "",
      valor_prejuizo: sinistro.valor_prejuizo ?? "",
      seguradora_acionada: sinistro.seguradora_acionada,
      status: sinistro.status,
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
    mutationFn: (valores: SinistroFormValues) =>
      apiClient.post("/sinistros", {
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
    mutationFn: (valores: SinistroFormValues) =>
      apiClient.patch(`/sinistros/${editandoId}`, {
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
    mutationFn: (id: string) => apiClient.delete(`/sinistros/${id}`),
    onSuccess: () => invalidar(),
  });

  function excluir(sinistro: Sinistro) {
    if (window.confirm(`Excluir este registro de sinistro (${ROTULOS_TIPO[sinistro.tipo]})?`)) {
      remover.mutate(sinistro.id);
    }
  }

  const podeRegistrar = hasPermission("sinistros:registrar");

  const columns = [
    columnHelper.accessor("data", { header: "Data", cell: (info) => formatarDataHora(info.getValue()) }),
    columnHelper.accessor("tipo", { header: "Tipo", cell: (info) => ROTULOS_TIPO[info.getValue()] }),
    columnHelper.accessor("descricao", { header: "Descrição", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("valor_prejuizo", {
      header: "Prejuízo",
      cell: (info) => (info.getValue() ? formatarMoeda(info.getValue() as string) : "—"),
    }),
    columnHelper.accessor("seguradora_acionada", {
      header: "Seguradora acionada",
      cell: (info) => (info.getValue() ? "Sim" : "Não"),
    }),
    columnHelper.accessor("status", { header: "Situação" }),
    ...(podeRegistrar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Sinistro } }) => {
              const sinistro = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(sinistro)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(sinistro)}
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
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Sinistros</h2>
        {podeRegistrar && (
          <Button
            variante="secundaria"
            onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}
          >
            {mostrarForm ? "Cancelar" : "Registrar sinistro"}
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
            <label className="mb-1 block text-sm font-medium text-slate-700">Tipo</label>
            <select className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("tipo")}>
              <option value="batida">Batida</option>
              <option value="roubo">Roubo</option>
              <option value="furto">Furto</option>
              <option value="enchente">Enchente</option>
              <option value="incendio">Incêndio</option>
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Data</label>
            <input type="date" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("data")} />
            {errors.data && <p className="text-xs text-red-600">{errors.data.message}</p>}
          </div>
          <div className="sm:col-span-2">
            <label className="mb-1 block text-sm font-medium text-slate-700">Descrição</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("descricao")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Valor do prejuízo</label>
            <input type="number" step="0.01" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("valor_prejuizo")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Situação</label>
            <select className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("status")}>
              <option value="aberto">Aberto</option>
              <option value="em_andamento">Em andamento</option>
              <option value="finalizado">Finalizado</option>
            </select>
          </div>
          <div className="flex items-end gap-2">
            <input type="checkbox" id="seguradora_acionada" {...register("seguradora_acionada")} />
            <label htmlFor="seguradora_acionada" className="text-sm text-slate-700">
              Seguradora acionada
            </label>
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar sinistro" : "Registrar sinistro"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os sinistros." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhum sinistro registrado para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <DataTable columns={columns} data={data} />
      )}
    </section>
  );
}
