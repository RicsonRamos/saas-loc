"""Guard de segurança do seed: recusa rodar fora de um banco de desenvolvimento local.

`settings.environment` não é confiável sozinho como sinal de "é seguro rodar aqui" —
nada no deploy define essa variável como "production", e é fácil ter DATABASE_URL de
produção configurada localmente sem perceber. Por isso a checagem principal é uma
allowlist do host do banco, não da env var.
"""

from sqlalchemy.engine import make_url

from app.core.config import settings

HOSTS_PERMITIDOS = {"localhost", "127.0.0.1", "db"}


class AmbienteInseguroError(RuntimeError):
    pass


def host_do_banco() -> str:
    return make_url(settings.database_url).host or ""


def nome_do_banco() -> str:
    return make_url(settings.database_url).database or ""


def garantir_ambiente_seguro(*, confirmar_automaticamente: bool) -> None:
    """Levanta AmbienteInseguroError se o banco não parecer um Postgres local de dev.

    Sem flag de override para produção: se o host não está na allowlist, não há
    como forçar a execução a partir daqui.
    """
    if settings.environment == "production":
        raise AmbienteInseguroError(
            "settings.environment está como 'production'. O seed nunca roda nesse ambiente."
        )

    host = host_do_banco()
    if host not in HOSTS_PERMITIDOS:
        raise AmbienteInseguroError(
            f"DATABASE_URL aponta para o host '{host}', que não é um Postgres local "
            f"reconhecido (permitidos: {sorted(HOSTS_PERMITIDOS)}). O seed só roda contra "
            "bancos de desenvolvimento locais — nunca contra produção."
        )

    banco = nome_do_banco()
    print(f"Banco alvo do seed: host='{host}' banco='{banco}'")
    print(
        "Atenção: este host pode ser tanto o Postgres do docker-compose quanto um "
        "Postgres nativo instalado na máquina, se ambos escutarem na mesma porta. "
        "Confirme que é o banco de desenvolvimento correto antes de prosseguir."
    )

    if confirmar_automaticamente:
        return

    resposta = input("Digite 'sim' para confirmar e continuar: ").strip().lower()
    if resposta != "sim":
        raise AmbienteInseguroError("Confirmação não recebida. Abortando.")
