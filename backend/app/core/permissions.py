"""Mapa simples de RBAC. Ver docs/03-AUTENTICACAO-AUTORIZACAO.md."""

ADMINISTRADOR = "administrador"
OPERADOR = "operador"
FINANCEIRO = "financeiro"
MECANICO = "mecanico"

ROLES = [ADMINISTRADOR, OPERADOR, FINANCEIRO, MECANICO]

ROLE_PERMISSIONS: dict[str, set[str]] = {
    ADMINISTRADOR: {"*"},
    OPERADOR: {
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
    },
    FINANCEIRO: {
        "frota:visualizar",
        "contratos:visualizar",
        "financeiro:visualizar",
        "financeiro:lancar",
        "financeiro:aprovar_estorno",
    },
    MECANICO: {
        "frota:visualizar",
        "manutencoes:visualizar",
        "manutencoes:registrar",
    },
}


def has_permission(role: str, permission: str) -> bool:
    granted = ROLE_PERMISSIONS.get(role, set())
    return "*" in granted or permission in granted
