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
        "multas:visualizar",
        "multas:registrar",
        "sinistros:visualizar",
        "sinistros:registrar",
        "danos:visualizar",
        "danos:registrar",
    },
    FINANCEIRO: {
        "frota:visualizar",
        "contratos:visualizar",
        "financeiro:visualizar",
        "financeiro:lancar",
        "financeiro:aprovar_estorno",
        "multas:visualizar",
        "sinistros:visualizar",
        "danos:visualizar",
    },
    MECANICO: {
        "frota:visualizar",
        "manutencoes:visualizar",
        "manutencoes:registrar",
        "sinistros:visualizar",
        "danos:visualizar",
        "danos:registrar",
    },
}


def has_permission(role: str, permission: str) -> bool:
    granted = ROLE_PERMISSIONS.get(role, set())
    return "*" in granted or permission in granted
