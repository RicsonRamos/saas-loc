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

const LIMITE_VEICULOS_NO_GRAFICO = 15;

function TotalCard({ rotulo, valor, cor }: { rotulo: string; valor: number; cor: string }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">{rotulo}</p>
      <p className={`mt-1 text-xl font-semibold ${cor}`}>{formatarMoeda(valor)}</p>
    </div>
  );
}

export function RentabilidadeChart({ dados }: { dados: RentabilidadeVeiculo[] }) {
  const totais = dados.reduce(
    (acumulado, item) => ({
      receita: acumulado.receita + Number(item.receita_total),
      despesa: acumulado.despesa + Number(item.despesa_total),
      resultado: acumulado.resultado + Number(item.resultado),
    }),
    { receita: 0, despesa: 0, resultado: 0 }
  );

  const dadosGrafico = [...dados]
    .sort((a, b) => Number(b.receita_total) - Number(a.receita_total))
    .slice(0, LIMITE_VEICULOS_NO_GRAFICO)
    .map((item) => ({
      placa: item.placa,
      Receita: Number(item.receita_total),
      Despesa: Number(item.despesa_total),
    }));

  const ocultos = dados.length - dadosGrafico.length;

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <TotalCard rotulo="Receita total da frota" valor={totais.receita} cor="text-emerald-700" />
        <TotalCard rotulo="Despesa total da frota" valor={totais.despesa} cor="text-red-700" />
        <TotalCard rotulo="Resultado total" valor={totais.resultado} cor="text-slate-900" />
      </div>

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
      <p className="text-xs text-slate-500">
        Mostrando os {dadosGrafico.length} veículos com maior receita
        {ocultos > 0 ? ` (${ocultos} de menor receita não exibidos no gráfico, mas incluídos nos totais acima).` : "."}
      </p>
    </div>
  );
}
