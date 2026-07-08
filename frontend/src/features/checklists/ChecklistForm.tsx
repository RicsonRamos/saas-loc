import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { SignaturePad } from "@/components/shared/SignaturePad";
import { apiClient, extrairMensagemErro } from "@/core/api/client";

import type { Checklist, ItemChecklist, SituacaoItemChecklist, TipoChecklist } from "./checklistTypes";

const ITENS: { valor: ItemChecklist; rotulo: string }[] = [
  { valor: "lataria", rotulo: "Lataria" },
  { valor: "pneus", rotulo: "Pneus" },
  { valor: "combustivel", rotulo: "Combustível" },
  { valor: "km", rotulo: "Quilometragem" },
  { valor: "documentos", rotulo: "Documentos" },
  { valor: "acessorios", rotulo: "Acessórios" },
];

const ROTULOS_SITUACAO: Record<SituacaoItemChecklist, string> = {
  ok: "OK",
  avaria: "Avaria",
  faltante: "Faltante",
};

type EstadoItens = Record<ItemChecklist, { situacao: SituacaoItemChecklist; observacao: string }>;

function itensIniciais(): EstadoItens {
  return Object.fromEntries(
    ITENS.map(({ valor }) => [valor, { situacao: "ok" as SituacaoItemChecklist, observacao: "" }])
  ) as EstadoItens;
}

const TITULOS: Record<TipoChecklist, string> = {
  entrega: "Checklist de entrega",
  devolucao: "Checklist de devolução",
};

export function ChecklistForm({
  contratoId,
  tipo,
  onConcluido,
  onCancelar,
}: {
  contratoId: string;
  tipo: TipoChecklist;
  onConcluido: () => void;
  onCancelar: () => void;
}) {
  const queryClient = useQueryClient();
  const [km, setKm] = useState("");
  const [combustivel, setCombustivel] = useState("");
  const [observacoesGerais, setObservacoesGerais] = useState("");
  const [itensEstado, setItensEstado] = useState<EstadoItens>(itensIniciais);
  const [checklistCriado, setChecklistCriado] = useState<Checklist | null>(null);
  const [responsavelNome, setResponsavelNome] = useState("");
  const [erro, setErro] = useState<string | null>(null);

  function atualizarItem(item: ItemChecklist, campo: "situacao" | "observacao", valor: string) {
    setItensEstado((atual) => ({ ...atual, [item]: { ...atual[item], [campo]: valor } }));
  }

  const criarChecklist = useMutation({
    mutationFn: () =>
      apiClient.post<Checklist>("/checklists", {
        contrato_id: contratoId,
        tipo,
        data: new Date().toISOString(),
        km: Number(km),
        combustivel: combustivel || null,
        observacoes_gerais: observacoesGerais || null,
        itens: ITENS.map(({ valor }) => ({
          item: valor,
          situacao: itensEstado[valor].situacao,
          observacao: itensEstado[valor].observacao || null,
        })),
      }),
    onSuccess: ({ data }) => {
      setChecklistCriado(data);
      setErro(null);
    },
    onError: (error) => setErro(extrairMensagemErro(error)),
  });

  const enviarAssinatura = useMutation({
    mutationFn: async (blob: Blob) => {
      if (!checklistCriado) throw new Error("Checklist ainda não foi criado.");
      const formData = new FormData();
      formData.append("arquivo", blob, "assinatura.png");
      formData.append("entidade_tipo", "assinatura");
      formData.append("entidade_id", checklistCriado.id);
      const { data: attachment } = await apiClient.post<{ id: string }>("/attachments", formData);
      await apiClient.post(`/checklists/${checklistCriado.id}/assinaturas`, {
        attachment_id: attachment.id,
        responsavel_nome: responsavelNome,
      });
    },
    onSuccess: () => {
      setErro(null);
      void queryClient.invalidateQueries({ queryKey: ["checklists", contratoId] });
      onConcluido();
    },
    onError: (error) => setErro(extrairMensagemErro(error)),
  });

  if (checklistCriado) {
    return (
      <div className="mb-6 rounded-lg border border-slate-200 bg-white p-4">
        <h3 className="mb-3 text-sm font-semibold text-slate-800">
          {TITULOS[tipo]} — assinatura do responsável
        </h3>
        <div className="mb-3">
          <label className="mb-1 block text-sm font-medium text-slate-700">
            Nome do responsável
          </label>
          <input
            className="w-full max-w-sm rounded-md border border-slate-300 px-3 py-2 text-sm"
            value={responsavelNome}
            onChange={(event) => setResponsavelNome(event.target.value)}
          />
        </div>
        <SignaturePad onAssinaturaPronta={(blob) => enviarAssinatura.mutate(blob)} />
        {erro && <p className="mt-2 text-sm text-red-600">{erro}</p>}
        {enviarAssinatura.isPending && (
          <p className="mt-2 text-sm text-slate-500">Enviando assinatura...</p>
        )}
      </div>
    );
  }

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        criarChecklist.mutate();
      }}
      className="mb-6 flex flex-col gap-4 rounded-lg border border-slate-200 bg-white p-4"
    >
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-800">{TITULOS[tipo]}</h3>
        <button type="button" className="text-xs text-slate-500 underline" onClick={onCancelar}>
          Cancelar
        </button>
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Quilometragem</label>
          <input
            type="number"
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            value={km}
            onChange={(event) => setKm(event.target.value)}
            required
          />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-700">Combustível</label>
          <select
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
            value={combustivel}
            onChange={(event) => setCombustivel(event.target.value)}
          >
            <option value="">—</option>
            <option value="vazio">Vazio</option>
            <option value="1/4">1/4</option>
            <option value="1/2">1/2</option>
            <option value="3/4">3/4</option>
            <option value="cheio">Cheio</option>
          </select>
        </div>
      </div>

      <div className="flex flex-col gap-2">
        {ITENS.map(({ valor, rotulo }) => (
          <div
            key={valor}
            className="grid grid-cols-1 items-center gap-2 rounded-md bg-slate-50 p-2 sm:grid-cols-3"
          >
            <span className="text-sm font-medium text-slate-700">{rotulo}</span>
            <select
              className="rounded-md border border-slate-300 px-2 py-1 text-sm"
              value={itensEstado[valor].situacao}
              onChange={(event) =>
                atualizarItem(valor, "situacao", event.target.value as SituacaoItemChecklist)
              }
            >
              {Object.entries(ROTULOS_SITUACAO).map(([situacao, rotuloSituacao]) => (
                <option key={situacao} value={situacao}>
                  {rotuloSituacao}
                </option>
              ))}
            </select>
            <input
              placeholder="Observação (opcional)"
              className="rounded-md border border-slate-300 px-2 py-1 text-sm"
              value={itensEstado[valor].observacao}
              onChange={(event) => atualizarItem(valor, "observacao", event.target.value)}
            />
          </div>
        ))}
      </div>

      <div>
        <label className="mb-1 block text-sm font-medium text-slate-700">
          Observações gerais
        </label>
        <textarea
          className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
          value={observacoesGerais}
          onChange={(event) => setObservacoesGerais(event.target.value)}
          rows={2}
        />
      </div>

      {erro && <p className="text-sm text-red-600">{erro}</p>}
      <div>
        <Button type="submit" disabled={criarChecklist.isPending}>
          {criarChecklist.isPending ? "Salvando..." : "Salvar checklist"}
        </Button>
      </div>
    </form>
  );
}
