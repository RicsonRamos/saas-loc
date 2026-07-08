/** Espelha app/core/permissions.py — só para esconder ações na UI. A autorização real é sempre no backend. */
export const ROLE_PERMISSIONS: Record<string, Set<string> | "*"> = {
  administrador: "*",
  operador: new Set([
    "frota:visualizar",
    "frota:editar",
    "clientes:visualizar",
    "clientes:editar",
    "motoristas:visualizar",
    "motoristas:editar",
    "contratos:visualizar",
    "contratos:emitir",
    "contratos:cancelar",
    "manutencoes:visualizar",
    "multas:visualizar",
    "multas:registrar",
    "sinistros:visualizar",
    "sinistros:registrar",
    "danos:visualizar",
    "danos:registrar",
    "abastecimentos:visualizar",
    "abastecimentos:registrar",
    "pneus:visualizar",
  ]),
  financeiro: new Set([
    "frota:visualizar",
    "contratos:visualizar",
    "financeiro:visualizar",
    "financeiro:lancar",
    "financeiro:aprovar_estorno",
    "multas:visualizar",
    "sinistros:visualizar",
    "danos:visualizar",
    "abastecimentos:visualizar",
    "pneus:visualizar",
  ]),
  mecanico: new Set([
    "frota:visualizar",
    "manutencoes:visualizar",
    "manutencoes:registrar",
    "sinistros:visualizar",
    "danos:visualizar",
    "danos:registrar",
    "abastecimentos:visualizar",
    "pneus:visualizar",
    "pneus:registrar",
  ]),
};

export function temPermissao(role: string | undefined, permissao: string): boolean {
  if (!role) return false;
  const permissoes = ROLE_PERMISSIONS[role];
  if (!permissoes) return false;
  if (permissoes === "*") return true;
  return permissoes.has(permissao);
}
