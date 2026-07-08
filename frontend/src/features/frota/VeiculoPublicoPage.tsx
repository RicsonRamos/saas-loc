import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";

import { ErrorState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";
import { formatarDataHora } from "@/core/format";

import type { VeiculoPublico } from "./veiculoPublicoTypes";

const ROTULOS_STATUS: Record<string, string> = {
  disponivel: "Disponível",
  alugado: "Alugado",
  reservado: "Reservado",
  em_manutencao: "Em manutenção",
  sinistrado: "Sinistrado",
  em_limpeza: "Em limpeza",
  licenciamento_vencido: "Licenciamento vencido",
  seguro_vencido: "Seguro vencido",
  inativo: "Inativo",
};

export function VeiculoPublicoPage() {
  const { codigo } = useParams<{ codigo: string }>();

  const { data, isLoading, isError } = useQuery({
    queryKey: ["veiculo-publico", codigo],
    queryFn: async () =>
      (await apiClient.get<VeiculoPublico>(`/veiculo/public/${codigo}`)).data,
    enabled: !!codigo,
    retry: false,
  });

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
      <div className="w-full max-w-sm rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        {isLoading && <LoadingState />}
        {isError && (
          <ErrorState mensagem="Veículo não encontrado ou código inválido." />
        )}
        {!isLoading && !isError && data && (
          <div className="flex flex-col gap-4">
            <div>
              <p className="text-2xl font-bold tracking-wide text-slate-900">{data.placa}</p>
              <p className="text-sm text-slate-500">
                {data.modelo} · {data.marca ?? "—"} · {data.ano}
              </p>
            </div>

            <div className="rounded-lg bg-slate-50 p-3">
              <p className="text-xs uppercase tracking-wide text-slate-500">Situação</p>
              <p className="text-sm font-semibold text-slate-900">
                {ROTULOS_STATUS[data.status] ?? data.status}
              </p>
            </div>

            <div className="rounded-lg bg-slate-50 p-3">
              <p className="text-xs uppercase tracking-wide text-slate-500">
                Quilometragem atual
              </p>
              <p className="text-sm font-semibold text-slate-900">{data.km_atual} km</p>
            </div>

            <div className="rounded-lg bg-slate-50 p-3">
              <p className="text-xs uppercase tracking-wide text-slate-500">Locação</p>
              <p className="text-sm font-semibold text-slate-900">
                {data.locacao_atual?.em_uso ? "Em uso" : "Disponível"}
              </p>
              {data.locacao_atual?.em_uso && data.locacao_atual.data_fim_prevista && (
                <p className="mt-1 text-xs text-slate-500">
                  Devolução prevista: {formatarDataHora(data.locacao_atual.data_fim_prevista)}
                </p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
