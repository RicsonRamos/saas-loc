import type { StatusVeiculo } from "./types";

const estilos: Record<StatusVeiculo, string> = {
  disponivel: "bg-emerald-100 text-emerald-700",
  alugado: "bg-red-100 text-red-700",
  reservado: "bg-yellow-100 text-yellow-800",
  em_manutencao: "bg-blue-100 text-blue-700",
  sinistrado: "bg-slate-800 text-white",
  em_limpeza: "bg-purple-100 text-purple-700",
  licenciamento_vencido: "bg-orange-100 text-orange-700",
  seguro_vencido: "bg-amber-100 text-amber-800",
  inativo: "bg-slate-100 text-slate-500",
};

const rotulos: Record<StatusVeiculo, string> = {
  disponivel: "🟢 Disponível",
  alugado: "🔴 Alugado",
  reservado: "🟡 Reservado",
  em_manutencao: "🔵 Em manutenção",
  sinistrado: "⚫ Sinistrado",
  em_limpeza: "🟣 Em limpeza",
  licenciamento_vencido: "🟠 Licenciamento vencido",
  seguro_vencido: "🔶 Seguro vencido",
  inativo: "⚪ Inativo",
};

export const STATUS_VEICULO_OPCOES: { valor: StatusVeiculo; rotulo: string }[] = (
  Object.keys(rotulos) as StatusVeiculo[]
).map((valor) => ({ valor, rotulo: rotulos[valor] }));

export function StatusVeiculoBadge({ status }: { status: StatusVeiculo }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${estilos[status]}`}>
      {rotulos[status]}
    </span>
  );
}
