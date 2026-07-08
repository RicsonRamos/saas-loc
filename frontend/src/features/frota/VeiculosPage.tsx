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

export function VeiculosPage() {
  const { hasPermission } = useAuth();
  const [page, setPage] = useState(1);
  const [mostrarForm, setMostrarForm] = useState(false);
  const [erroForm, setErroForm] = useState<string | null>(null);
  const [erroAcao, setErroAcao] = useState<string | null>(null);
  const [editandoId, setEditandoId] = useState<string | null>(null);
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

  function invalidar() {
    void queryClient.invalidateQueries({ queryKey: ["veiculos"] });
  }

  function abrirNovo() {
    setEditandoId(null);
    reset({ km_atual: 0 });
    setErroForm(null);
    setMostrarForm(true);
  }

  function abrirEdicao(veiculo: Veiculo) {
    setEditandoId(veiculo.id);
    reset({
      placa: veiculo.placa,
      modelo: veiculo.modelo,
      ano: veiculo.ano,
      km_atual: veiculo.km_atual,
      marca: veiculo.marca ?? "",
      cor: veiculo.cor ?? "",
      categoria: veiculo.categoria ?? "",
      chassi: veiculo.chassi ?? "",
      renavam: veiculo.renavam ?? "",
      combustivel: veiculo.combustivel ?? "",
      cambio: veiculo.cambio ?? "",
      vencimento_licenciamento: veiculo.vencimento_licenciamento ?? "",
      vencimento_seguro: veiculo.vencimento_seguro ?? "",
    });
    setErroForm(null);
    setMostrarForm(true);
  }

  function fecharForm() {
    setMostrarForm(false);
    setEditandoId(null);
    reset({ km_atual: 0 });
    setErroForm(null);
  }

  const criarVeiculo = useMutation({
    mutationFn: (valores: VeiculoFormValues) => apiClient.post("/veiculos", valores),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const atualizarVeiculo = useMutation({
    mutationFn: (valores: VeiculoFormValues) =>
      apiClient.patch(`/veiculos/${editandoId}`, {
        modelo: valores.modelo,
        ano: valores.ano,
        km_atual: valores.km_atual,
        marca: valores.marca,
        cor: valores.cor,
        categoria: valores.categoria,
        chassi: valores.chassi,
        renavam: valores.renavam,
        combustivel: valores.combustivel,
        cambio: valores.cambio,
        vencimento_licenciamento: valores.vencimento_licenciamento,
        vencimento_seguro: valores.vencimento_seguro,
      }),
    onSuccess: () => {
      invalidar();
      fecharForm();
    },
    onError: (error) => setErroForm(extrairMensagemErro(error)),
  });

  const removerVeiculo = useMutation({
    mutationFn: (veiculoId: string) => apiClient.delete(`/veiculos/${veiculoId}`),
    onSuccess: () => {
      invalidar();
      setErroAcao(null);
    },
    onError: (error) => setErroAcao(extrairMensagemErro(error)),
  });

  function excluir(veiculo: Veiculo) {
    if (window.confirm(`Excluir o veículo ${veiculo.placa}?`)) {
      removerVeiculo.mutate(veiculo.id);
    }
  }

  const podeEditar = hasPermission("frota:editar");

  const columns = [
    columnHelper.accessor("placa", { header: "Placa" }),
    columnHelper.accessor("modelo", { header: "Modelo" }),
    columnHelper.accessor("marca", { header: "Marca", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("ano", { header: "Ano" }),
    columnHelper.accessor("cor", { header: "Cor", cell: (info) => info.getValue() ?? "—" }),
    columnHelper.accessor("categoria", {
      header: "Categoria",
      cell: (info) => info.getValue() ?? "—",
    }),
    columnHelper.accessor("km_atual", { header: "KM atual" }),
    columnHelper.accessor("status", {
      header: "Status",
      cell: (info) => <StatusVeiculoBadge status={info.getValue()} />,
    }),
    ...(podeEditar
      ? [
          columnHelper.display({
            id: "acoes",
            header: "Ações",
            cell: (info: { row: { original: Veiculo } }) => {
              const veiculo = info.row.original;
              return (
                <div className="flex gap-2">
                  <button
                    className="text-xs text-blue-700 underline"
                    onClick={() => abrirEdicao(veiculo)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-xs text-red-700 underline"
                    onClick={() => excluir(veiculo)}
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
    <div>
      <PageHeader
        title="Frota"
        actions={
          podeEditar && (
            <Button onClick={() => (mostrarForm ? fecharForm() : abrirNovo())}>
              {mostrarForm ? "Cancelar" : "Novo veículo"}
            </Button>
          )
        }
      />

      {mostrarForm && (
        <form
          onSubmit={handleSubmit((valores) =>
            editandoId ? atualizarVeiculo.mutate(valores) : criarVeiculo.mutate(valores)
          )}
          className="mb-6 grid grid-cols-1 gap-3 rounded-lg border border-slate-200 bg-white p-4 sm:grid-cols-4"
        >
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Placa</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm disabled:bg-slate-100"
              disabled={!!editandoId}
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
            <label className="mb-1 block text-sm font-medium text-slate-700">Marca</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("marca")}
            />
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
            <label className="mb-1 block text-sm font-medium text-slate-700">Cor</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("cor")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Categoria</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              placeholder="Ex.: Hatch, SUV, Pickup"
              {...register("categoria")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">KM atual</label>
            <input
              type="number"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("km_atual")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Combustível</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("combustivel")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Câmbio</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("cambio")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Chassi</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("chassi")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">RENAVAM</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("renavam")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Vencimento do licenciamento
            </label>
            <input
              type="date"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("vencimento_licenciamento")}
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Vencimento do seguro
            </label>
            <input
              type="date"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              {...register("vencimento_seguro")}
            />
          </div>
          {erroForm && <p className="col-span-full text-sm text-red-600">{erroForm}</p>}
          <div className="col-span-full">
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Salvando..." : editandoId ? "Atualizar veículo" : "Salvar veículo"}
            </Button>
          </div>
        </form>
      )}

      {erroAcao && <p className="mb-3 text-sm text-red-600">{erroAcao}</p>}

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
