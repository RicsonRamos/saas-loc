import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/States";
import { FileUpload } from "@/components/shared/FileUpload";
import { apiClient, extrairMensagemErro } from "@/core/api/client";
import { useAuth } from "@/core/auth/AuthContext";
import { formatarDataHora } from "@/core/format";

import type { Anexo } from "./anexoTypes";

function formatarTamanho(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function AnexosSecao({ veiculoId }: { veiculoId: string }) {
  const { hasPermission } = useAuth();
  const [erro, setErro] = useState<string | null>(null);
  const queryClient = useQueryClient();

  const podeVisualizar = hasPermission("anexos:visualizar");
  const podeEnviar = hasPermission("anexos:enviar");
  const podeExcluir = hasPermission("anexos:excluir");

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["attachments", { entidade_tipo: "veiculo", entidade_id: veiculoId }],
    queryFn: async () =>
      (
        await apiClient.get<{ data: Anexo[] }>("/attachments", {
          params: { entidade_tipo: "veiculo", entidade_id: veiculoId, limit: 100 },
        })
      ).data.data,
    enabled: podeVisualizar,
  });

  function invalidar() {
    void queryClient.invalidateQueries({
      queryKey: ["attachments", { entidade_tipo: "veiculo", entidade_id: veiculoId }],
    });
  }

  const enviar = useMutation({
    mutationFn: (arquivo: File) => {
      const formData = new FormData();
      formData.append("arquivo", arquivo);
      formData.append("entidade_tipo", "veiculo");
      formData.append("entidade_id", veiculoId);
      return apiClient.post("/attachments", formData);
    },
    onSuccess: () => {
      setErro(null);
      invalidar();
    },
    onError: (error) => setErro(extrairMensagemErro(error)),
  });

  const remover = useMutation({
    mutationFn: (anexoId: string) => apiClient.delete(`/attachments/${anexoId}`),
    onSuccess: () => invalidar(),
    onError: (error) => setErro(extrairMensagemErro(error)),
  });

  async function baixar(anexo: Anexo) {
    try {
      const { data } = await apiClient.get<{ url: string }>(`/attachments/${anexo.id}/download`);
      window.open(data.url, "_blank");
    } catch (error) {
      setErro(extrairMensagemErro(error));
    }
  }

  function excluir(anexo: Anexo) {
    if (window.confirm(`Excluir o anexo "${anexo.nome_original}"?`)) {
      remover.mutate(anexo.id);
    }
  }

  if (!podeVisualizar) return null;

  return (
    <section>
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Anexos</h2>
        {podeEnviar && (
          <FileUpload
            disabled={enviar.isPending}
            onArquivoSelecionado={(arquivo) => enviar.mutate(arquivo)}
          />
        )}
      </div>

      {erro && <p className="mb-2 text-sm text-red-600">{erro}</p>}
      {enviar.isPending && <p className="mb-2 text-sm text-slate-500">Enviando arquivo...</p>}

      {isLoading && <LoadingState />}
      {isError && (
        <ErrorState mensagem="Não foi possível carregar os anexos." aoTentarNovamente={() => refetch()} />
      )}
      {!isLoading && !isError && data && data.length === 0 && (
        <EmptyState mensagem="Nenhum anexo cadastrado para este veículo." />
      )}
      {!isLoading && !isError && data && data.length > 0 && (
        <ul className="flex flex-col gap-2">
          {data.map((anexo) => (
            <li
              key={anexo.id}
              className="flex items-center justify-between gap-3 rounded-lg border border-slate-200 bg-white p-3"
            >
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-slate-800">
                  {anexo.nome_original}
                </p>
                <p className="text-xs text-slate-500">
                  {formatarTamanho(anexo.tamanho_bytes)} · {formatarDataHora(anexo.data_upload)}
                </p>
              </div>
              <div className="flex shrink-0 gap-2">
                <Button variante="secundaria" onClick={() => baixar(anexo)}>
                  Baixar
                </Button>
                {podeExcluir && (
                  <Button variante="perigo" onClick={() => excluir(anexo)}>
                    Excluir
                  </Button>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
