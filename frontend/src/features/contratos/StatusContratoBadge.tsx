import type { StatusContrato } from "./types";

const estilos: Record<StatusContrato, string> = {
  reservado: "bg-slate-200 text-slate-700",
  ativo: "bg-blue-100 text-blue-700",
  encerrado: "bg-emerald-100 text-emerald-700",
  cancelado: "bg-red-100 text-red-700",
};

const rotulos: Record<StatusContrato, string> = {
  reservado: "Reservado",
  ativo: "Ativo",
  encerrado: "Encerrado",
  cancelado: "Cancelado",
};

export function StatusContratoBadge({ status }: { status: StatusContrato }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${estilos[status]}`}>
      {rotulos[status]}
    </span>
  );
}
