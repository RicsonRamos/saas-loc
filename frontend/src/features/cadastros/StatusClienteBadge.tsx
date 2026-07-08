import type { StatusCliente } from "./types";

const estilos: Record<StatusCliente, string> = {
  ativo: "bg-emerald-100 text-emerald-700",
  bloqueado: "bg-yellow-100 text-yellow-800",
  inadimplente: "bg-red-100 text-red-700",
  em_analise: "bg-blue-100 text-blue-700",
  inativo: "bg-slate-100 text-slate-500",
};

const rotulos: Record<StatusCliente, string> = {
  ativo: "🟢 Ativo",
  bloqueado: "🟡 Bloqueado",
  inadimplente: "🔴 Inadimplente",
  em_analise: "🔵 Em análise",
  inativo: "⚫ Inativo",
};

export const STATUS_CLIENTE_OPCOES: { valor: StatusCliente; rotulo: string }[] = (
  Object.keys(rotulos) as StatusCliente[]
).map((valor) => ({ valor, rotulo: rotulos[valor] }));

export function StatusClienteBadge({ status }: { status: StatusCliente }) {
  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${estilos[status]}`}>
      {rotulos[status]}
    </span>
  );
}
