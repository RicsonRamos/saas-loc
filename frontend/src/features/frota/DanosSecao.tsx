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

import { danoSchema, type DanoFormInput, type DanoFormValues } from "./incidentesSchema";
import type { Dano } from "./incidentesTypes";

const columnHelper = createColumnHelper<Dano>();

const CAMPOS_VAZIOS: DanoFormInput = {
  tipo: "arranhao",
  descricao: "",
  data: "",
  valor_reparo: "",
  status: "pendente",
};

const ROTULOS_TIPO: Record<string, string> = {
  arranhao: "Arranhão",
  amassado: "Amassado",
  quebra_vidro: "Quebra de vidro",
  dano_interno: "Dano interno",
  outro: "Outro",
};

export function DanosSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["danos", { veiculo_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: Dano[] }>("/danos", {
          params: { veiculo_id: veiculoId, limit: 100 },
        })
      ).data.data,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<DanoFormInput, unknown, DanoFormValues>({
    resolver: zodResolver(danoSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["danos", { veiculo_id: veiculoId }] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(dano: Dano) {
    setEditandoId(dano.id);
    reset({
      tipo: dano.tipo,
      descricao: dano.descricao ?? "",
      data: dano.data.slice(0, 10),
      valor_reparo: dano.valor_reparo ?? "",
      status: dano.status,
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
    mutationFn: (valores: DanoFormValues) =>
      apiClient.post("/danos", { ...valores, veiculo_id: veiculoId }),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizar = useMutation({
    mutationFn: (valores: DanoFormValues) => apiClient.patch(`/danos/${editandoId}`, valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const remover = useMutation({
    mutationFn: (id: string) => apiClient.delete(`/danos/${id}`),
    onSuccess: () => invalidar(),
  });

  function excluir(dano: Dano) {
    if (window.confirm(`Excluir este registro de dano (${ROTULOS_TIPO[dano.tipo]})?`)) {
      remover.mutate(dano.id);
    }
  }

  const podeRegistrar = hasPermission("danos:registrar");

  const columns = [
    columnHelper.accessor("data", { header: "Data", cell: (info) => formatarData(info.getValue()) }),
    columnHelper.accessor("tipo", { header: "Tipo", cell: (info) => ROTULOS_TIPO[info.getValue()] }),
    columnHelper.accessor("descricao", { header: "Descrição", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("valor_reparo", {
      header: "Valor do reparo",
      cell: (info) => (info.getValue() ? formatarMoeda(info.getValue() as string) : "—"),
    }),
    columnHelper.accessor("status", { header: "Situação" }),
    ...(podeRegistrar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Dano } }) => {
              const dano = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(dano)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(dano)}
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
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Danos</h2>
        {podeRegistrar && (
          <Button
            variante="secundaria"
            onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}
          >
            {mostrarForm ? "Cancelar" : "Registrar dano"}
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
              <option value="arranhao">Arranhão</option>
              <option value="amassado">Amassado</option>
              <option value="quebra_vidro">Quebra de vidro</option>
              <option value="dano_interno">Dano interno</option>
              <option value="outro">Outro</option>
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
            <label className="mb-1 block text-sm font-medium text-slate-700">Valor do reparo</label>
            <input type="number" step="0.01" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("valor_reparo")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Situação</label>
            <select className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("status")}>
              <option value="pendente">Pendente</option>
              <option value="reparado">Reparado</option>
            </select>
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar dano" : "Registrar dano"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os danos." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhum dano registrado para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <DataTable columns={columns} data={data} />
      )}
    </section>
  );
}
