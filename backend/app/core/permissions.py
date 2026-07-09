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
        "frota:regenerar_codigo_publico",
        "auditoria:visualizar",
        "anexos:visualizar",
        "anexos:enviar",
        "anexos:excluir",
        "checklists:visualizar",
        "checklists:registrar",
        "clientes:visualizar",
        "clientes:editar",
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
        "leituras_km:visualizar",
        "leituras_km:registrar",
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
        "abastecimentos:visualizar",
        "pneus:visualizar",
        "anexos:visualizar",
    },
    MECANICO: {
        "frota:visualizar",
        "manutencoes:visualizar",
        "manutencoes:registrar",
        "sinistros:visualizar",
        "danos:visualizar",
        "danos:registrar",
        "abastecimentos:visualizar",
        "pneus:visualizar",
        "pneus:registrar",
        "anexos:visualizar",
        "anexos:enviar",
        "checklists:visualizar",
        "leituras_km:visualizar",
        "leituras_km:registrar",
    },
}


def has_permission(role: str, permission: str) -> bool:
    granted = ROLE_PERMISSIONS.get(role, set())
    return "*" in granted or permission in granted
