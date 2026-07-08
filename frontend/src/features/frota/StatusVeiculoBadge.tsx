import type { StatusVeiculo } from "./types";

const estilos: Record<StatusVeiculo, string> = {
  disponivel: "bg-emerald-100 text-emerald-700",
  alugado: "bg-blue-100 text-blue-700",
  em_manutencao: "bg-amber-100 text-amber-700",
  baixado: "bg-slate-200 text-slate-600",
};

const rotulos: Record<StatusVeiculo, string> = {
  disponivel: "Disponível",
  alugado: "Alugado",
  em_manutencao: "Em manutenção",
  baixado: "Baixado",
};

export function StatusVeiculoBadge({ status }: { status: StatusVeiculo }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${estilos[status]}`}>
      {rotulos[status]}
    </span>
  );
}
