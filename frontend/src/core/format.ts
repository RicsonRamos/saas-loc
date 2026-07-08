export function formatarMoeda(valor: number | string): string {
  const numero = typeof valor === "string" ? Number(valor) : valor;
  return numero.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

export function formatarData(valor: string | Date): string {
  const data = typeof valor === "string" ? new Date(valor) : valor;
  return data.toLocaleDateString("pt-BR");
}

export function formatarDataHora(valor: string | Date): string {
  const data = typeof valor === "string" ? new Date(valor) : valor;
  return data.toLocaleString("pt-BR");
}
