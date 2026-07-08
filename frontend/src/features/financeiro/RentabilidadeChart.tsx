import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { formatarMoeda } from "@/core/format";

import type { RentabilidadeVeiculo } from "./types";

export function RentabilidadeChart({ dados }: { dados: RentabilidadeVeiculo[] }) {
  const dadosGrafico = dados.map((item) => ({
    placa: item.placa,
    Receita: Number(item.receita_total),
    Despesa: Number(item.despesa_total),
  }));

  return (
    <div className="h-80 rounded-lg border border-slate-200 bg-white p-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={dadosGrafico}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="placa" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip formatter={(valor) => formatarMoeda(Number(valor))} />
          <Legend />
          <Bar dataKey="Receita" fill="#0f172a" radius={[4, 4, 0, 0]} />
          <Bar dataKey="Despesa" fill="#dc2626" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
