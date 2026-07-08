import { useState, type ChangeEvent } from "react";

interface FileUploadProps {
  onArquivoSelecionado: (arquivo: File) => void;
  aceitar?: string;
  disabled?: boolean;
}

export function FileUpload({
  onArquivoSelecionado,
  aceitar = "image/jpeg,image/png,image/webp,application/pdf",
  disabled,
}: FileUploadProps) {
  const [nomeArquivo, setNomeArquivo] = useState<string | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  function aoSelecionar(event: ChangeEvent<HTMLInputElement>) {
    const arquivo = event.target.files?.[0];
    if (!arquivo) return;
    setNomeArquivo(arquivo.name);
    setPreviewUrl(arquivo.type.startsWith("image/") ? URL.createObjectURL(arquivo) : null);
    onArquivoSelecionado(arquivo);
    event.target.value = "";
  }

  return (
    <div className="flex items-center gap-3">
      <input
        type="file"
        accept={aceitar}
        disabled={disabled}
        onChange={aoSelecionar}
        className="text-sm text-slate-700 file:mr-3 file:rounded-md file:border-0 file:bg-slate-900 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-slate-700 disabled:opacity-50"
      />
      {previewUrl && (
        <img src={previewUrl} alt="Pré-visualização" className="h-10 w-10 rounded object-cover" />
      )}
      {nomeArquivo && !previewUrl && <span className="text-xs text-slate-500">{nomeArquivo}</span>}
    </div>
  );
}
