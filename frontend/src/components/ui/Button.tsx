import type { ButtonHTMLAttributes } from "react";

type Variante = "primaria" | "secundaria" | "perigo";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variante?: Variante;
}

const estilos: Record<Variante, string> = {
  primaria: "bg-slate-900 text-white hover:bg-slate-700",
  secundaria: "bg-white text-slate-900 border border-slate-300 hover:bg-slate-100",
  perigo: "bg-red-600 text-white hover:bg-red-700",
};

export function Button({ variante = "primaria", className = "", ...props }: ButtonProps) {
  return (
    <button
      className={`rounded-md px-4 py-2 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50 ${estilos[variante]} ${className}`}
      {...props}
    />
  );
}
