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
import { formatarData } from "@/core/format";

import { condutorSchema, type CondutorFormInput, type CondutorFormValues } from "./schema";
import type { Motorista } from "./types";

const columnHelper = createColumnHelper<Motorista>();

const CAMPOS_VAZIOS: CondutorFormInput = {
  nome: "",
  cnh: "",
  validade_cnh: "",
  telefone: "",
  parentesco: "",
};

export function CondutoresSecao({ clienteId }: { clienteId: string }) {
  const { hasPermission } = useAuth();
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["motoristas", { cliente_id: clienteId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: Motorista[] }>("/motoristas", {
          params: { cliente_id: clienteId, limit: 100 },
        })
      ).data.data,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CondutorFormInput, unknown, CondutorFormValues>({
    resolver: zodResolver(condutorSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["motoristas", { cliente_id: clienteId }] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(condutor: Motorista) {
    setEditandoId(condutor.id);
    reset({
      nome: condutor.nome,
      cnh: condutor.cnh,
      validade_cnh: condutor.validade_cnh,
      telefone: condutor.telefone ?? "",
      parentesco: condutor.parentesco ?? "",
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
    mutationFn: (valores: CondutorFormValues) =>
      apiClient.post("/motoristas", { ...valores, cliente_id: clienteId }),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizar = useMutation({
    mutationFn: (valores: CondutorFormValues) =>
      apiClient.patch(`/motoristas/${editandoId}`, valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const remover = useMutation({
    mutationFn: (id: string) => apiClient.delete(`/motoristas/${id}`),
    onSuccess: () => invalidar(),
  });

  function excluir(condutor: Motorista) {
    if (window.confirm(`Excluir o condutor ${condutor.nome}?`)) {
      remover.mutate(condutor.id);
    }
  }

  const podeEditar = hasPermission("motoristas:editar");

  const columns = [
    columnHelper.accessor("nome", { header: "Nome" }),
    columnHelper.accessor("cnh", { header: "CNH" }),
    columnHelper.accessor("validade_cnh", {
      header: "Validade da CNH",
      cell: (info) => formatarData(info.getValue()),
    }),
    columnHelper.accessor("telefone", { header: "Telefone", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("parentesco", {
      header: "Vínculo",
      cell: (info) => info.getValue() ?? "—",
    }),
    ...(podeEditar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Motorista } }) => {
              const condutor = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(condutor)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(condutor)}
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
          Condutores autorizados / dependentes
        </h2>
        {podeEditar && (
          <Button
            variante="secundaria"
            onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}
          >
            {mostrarForm ? "Cancelar" : "Novo condutor"}
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
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("telefone")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Vínculo (parentesco ou função)
            </label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              placeholder="Ex.: Cônjuge, Filho(a), Funcionário autorizado"
              {...register("parentesco")}
            />
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar condutor" : "Salvar condutor"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os condutores." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhum condutor adicional cadastrado para este cliente." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <DataTable columns={columns} data={data} />
      )}
    </section>
  );
}
