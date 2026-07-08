import { useQuery } from "@tanstack/react-query";

import { EmptyState, LoadingState } from "@/components/ui/States";
import { apiClient } from "@/core/api/client";

import type { ChecklistComparacao as ChecklistComparacaoTipo } from "./checklistTypes";

const ROTULOS_ITEM: Record<string, string> = {
  lataria: "Lataria",
  pneus: "Pneus",
  combustivel: "Combustível",
  km: "Quilometragem",
  documentos: "Documentos",
  acessorios: "Acessórios",
};

const ROTULOS_SITUACAO: Record<string, string> = {
  ok: "OK",
  avaria: "Avaria",
  faltante: "Faltante",
};

export function ChecklistComparacao({ contratoId }: { contratoId: string }) {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["checklists", contratoId, "comparacao"],
    queryFn: async () =>
      (
        await apiClient.get<ChecklistComparacaoTipo>(
          `/contratos/${contratoId}/checklists/comparacao`
        )
      ).data,
    retry: false,
  });

  if (isLoading) return <LoadingState />;
  if (isError) {
    return (
      <EmptyState mensagem="Comparação indisponível: registre os checklists de entrega e devolução para este contrato." />
    );
  }
  if (!data) return null;

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200">
      <table className="w-full text-sm">
        <thead className="bg-slate-900 text-white">
          <tr>
            <th className="px-3 py-2 text-left">Item</th>
            <th className="px-3 py-2 text-left">Entrega</th>
            <th className="px-3 py-2 text-left">Devolução</th>
            <th className="px-3 py-2 text-left">Mudou?</th>
          </tr>
        </thead>
        <tbody>
          {data.itens.map((item) => (
            <tr
              key={item.item}
              className={item.mudou ? "bg-amber-50" : "odd:bg-white even:bg-slate-50"}
            >
              <td className="px-3 py-2 font-medium text-slate-800">
                {ROTULOS_ITEM[item.item] ?? item.item}
              </td>
              <td className="px-3 py-2">
                {item.situacao_entrega ? ROTULOS_SITUACAO[item.situacao_entrega] : "—"}
              </td>
              <td className="px-3 py-2">
                {item.situacao_devolucao ? ROTULOS_SITUACAO[item.situacao_devolucao] : "—"}
              </td>
              <td className="px-3 py-2">{item.mudou ? "Sim" : "Não"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
