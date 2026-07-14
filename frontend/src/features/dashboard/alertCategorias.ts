import type { Alerta, PrioridadeAlerta } from "./types";

export type ChaveCategoriaAlerta = "documentos" | "manutencao" | "contratos" | "financeiro";

const ROTULO_POR_CATEGORIA: Record<ChaveCategoriaAlerta, string> = {
  documentos: "Documentos",
  manutencao: "Manutenção",
  contratos: "Contratos",
  financeiro: "Financeiro",
};

const PESO_PRIORIDADE: Record<PrioridadeAlerta, number> = {
  critico: 2,
  atencao: 1,
  normal: 0,
};

function categoriaDoTipo(tipo: string): ChaveCategoriaAlerta {
  if (tipo.startsWith("seguro_") || tipo.startsWith("licenciamento_")) return "documentos";
  if (tipo.startsWith("revisao_") || tipo.startsWith("manutencao_")) return "manutencao";
  if (
    tipo === "devolucao_hoje" ||
    tipo === "franquia_km_excedida" ||
    tipo === "franquia_km_proxima"
  ) {
    return "contratos";
  }
  return "financeiro";
}

export interface CategoriaAlertas {
  chave: ChaveCategoriaAlerta;
  rotulo: string;
  prioridadeMax: PrioridadeAlerta;
  alertas: Alerta[];
}

export function categorizarAlertas(alertas: Alerta[]): CategoriaAlertas[] {
  const porCategoria = new Map<ChaveCategoriaAlerta, Alerta[]>();

  for (const alerta of alertas) {
    const chave = categoriaDoTipo(alerta.tipo);
    const lista = porCategoria.get(chave) ?? [];
    lista.push(alerta);
    porCategoria.set(chave, lista);
  }

  const categorias: CategoriaAlertas[] = Array.from(porCategoria.entries()).map(
    ([chave, itens]) => ({
      chave,
      rotulo: ROTULO_POR_CATEGORIA[chave],
      prioridadeMax: itens.reduce<PrioridadeAlerta>(
        (max, item) => (PESO_PRIORIDADE[item.prioridade] > PESO_PRIORIDADE[max] ? item.prioridade : max),
        "normal"
      ),
      alertas: itens,
    })
  );

  return categorias.sort((a, b) => PESO_PRIORIDADE[b.prioridadeMax] - PESO_PRIORIDADE[a.prioridadeMax]);
}
