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

import { pneuSchema, type PneuFormInput, type PneuFormValues } from "./abastecimentoPneuSchema";
import type { Pneu } from "./abastecimentoPneuTypes";

const columnHelper = createColumnHelper<Pneu>();

const CAMPOS_VAZIOS: PneuFormInput = {
  marca: "",
  modelo: "",
  numero_serie: "",
  posicao: "dianteiro_esquerdo",
  data_instalacao: "",
  km_instalacao: 0,
  vida_util_km: "",
  data_troca: "",
  km_troca: "",
  status: "ativo",
};

const ROTULOS_POSICAO: Record<string, string> = {
  dianteiro_esquerdo: "Dianteiro esquerdo",
  dianteiro_direito: "Dianteiro direito",
  traseiro_esquerdo: "Traseiro esquerdo",
  traseiro_direito: "Traseiro direito",
  estepe: "Estepe",
};

export function PneusSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["pneus", { veiculo_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: Pneu[] }>("/pneus", {
          params: { veiculo_id: veiculoId, limit: 100 },
        })
      ).data.data,
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<PneuFormInput, unknown, PneuFormValues>({
    resolver: zodResolver(pneuSchema),
    defaultValues: CAMPOS_VAZIOS,
  });

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["pneus", { veiculo_id: veiculoId }] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset(CAMPOS_VAZIOS);
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(pneu: Pneu) {
    setEditandoId(pneu.id);
    reset({
      marca: pneu.marca,
      modelo: pneu.modelo ?? "",
      numero_serie: pneu.numero_serie ?? "",
      posicao: pneu.posicao,
      data_instalacao: pneu.data_instalacao,
      km_instalacao: pneu.km_instalacao,
      vida_util_km: pneu.vida_util_km != null ? String(pneu.vida_util_km) : "",
      data_troca: pneu.data_troca ?? "",
      km_troca: pneu.km_troca != null ? String(pneu.km_troca) : "",
      status: pneu.status,
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
    mutationFn: (valores: PneuFormValues) =>
      apiClient.post("/pneus", { ...valores, veiculo_id: veiculoId }),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizar = useMutation({
    mutationFn: (valores: PneuFormValues) => apiClient.patch(`/pneus/${editandoId}`, valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const remover = useMutation({
    mutationFn: (id: string) => apiClient.delete(`/pneus/${id}`),
    onSuccess: () => invalidar(),
  });

  function excluir(pneu: Pneu) {
    if (window.confirm(`Excluir o registro do pneu ${ROTULOS_POSICAO[pneu.posicao]}?`)) {
      remover.mutate(pneu.id);
    }
  }

  const podeRegistrar = hasPermission("pneus:registrar");

  const columns = [
    columnHelper.accessor("posicao", {
      header: "Posição",
      cell: (info) => ROTULOS_POSICAO[info.getValue()],
    }),
    columnHelper.accessor("marca", { header: "Marca" }),
    columnHelper.accessor("modelo", { header: "Modelo", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("data_instalacao", {
      header: "Instalação",
      cell: (info) => formatarData(info.getValue()),
    }),
    columnHelper.accessor("km_instalacao", { header: "KM instalação" }),
    columnHelper.accessor("status", {
      header: "Situação",
      cell: (info) => (info.getValue() === "ativo" ? "Ativo" : "Trocado"),
    }),
    ...(podeRegistrar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Pneu } }) => {
              const pneu = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(pneu)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(pneu)}
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
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Pneus</h2>
        {podeRegistrar && (
          <Button
            variante="secundaria"
            onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}
          >
            {mostrarForm ? "Cancelar" : "Novo pneu"}
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
            <label className="mb-1 block text-sm font-medium text-slate-700">Posição</label>
            <select className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("posicao")}>
              {Object.entries(ROTULOS_POSICAO).map(([valor, rotulo]) => (
                <option key={valor} value={valor}>
                  {rotulo}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Marca</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("marca")} />
            {errors.marca && <p className="text-xs text-red-600">{errors.marca.message}</p>}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Modelo</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("modelo")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Número de série</label>
            <input className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("numero_serie")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Data de instalação</label>
            <input type="date" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("data_instalacao")} />
            {errors.data_instalacao && (
              <p className="text-xs text-red-600">{errors.data_instalacao.message}</p>
            )}
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">KM de instalação</label>
            <input type="number" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("km_instalacao")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Vida útil (KM)</label>
            <input type="number" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("vida_util_km")} />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Situação</label>
            <select className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("status")}>
              <option value="ativo">Ativo</option>
              <option value="trocado">Trocado</option>
            </select>
          </div>
          {editandoId && (
            <>
              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">Data da troca</label>
                <input type="date" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("data_troca")} />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">KM da troca</label>
                <input type="number" className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm" {...register("km_troca")} />
              </div>
            </>
          )}
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar pneu" : "Salvar pneu"}
            </Button>
          </div>
        </form>
      )}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os pneus." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhum pneu cadastrado para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <DataTable columns={columns} data={data} />
      )}
    </section>
  );
}
