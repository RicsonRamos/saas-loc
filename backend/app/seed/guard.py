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


def garantir_ambiente_seguro(
    *, confirmar_automaticamente: bool, host_extra_permitido: str | None = None
) -> None:
    """Levanta AmbienteInseguroError se o banco não parecer seguro para o seed.

    `host_extra_permitido` é uma exceção pontual (vem de `--permitir-host <host>` na
    CLI): só libera um host fora da allowlist se o valor bater EXATAMENTE com o host
    resolvido — não existe um "--force" genérico, o host tem que ser digitado
    explicitamente a cada execução. Use só para bancos remotos que você tem certeza
    de que não têm dados reais (ex.: um projeto Supabase de desenvolvimento/demo).
    """
    if settings.environment == "production":
        raise AmbienteInseguroError(
            "settings.environment está como 'production'. O seed nunca roda nesse ambiente."
        )

    host = host_do_banco()
    excecao_valida = host_extra_permitido is not None and host_extra_permitido == host

    if host not in HOSTS_PERMITIDOS and not excecao_valida:
        raise AmbienteInseguroError(
            f"DATABASE_URL aponta para o host '{host}', que não é um Postgres local "
            f"reconhecido (permitidos: {sorted(HOSTS_PERMITIDOS)}). O seed só roda contra "
            "bancos de desenvolvimento locais — nunca contra produção. Se tiver certeza "
            "de que este host é seguro para popular com dados fictícios (sem dados reais "
            f"de clientes/operação), rode de novo com --permitir-host {host!r}."
        )

    banco = nome_do_banco()
    print(f"Banco alvo do seed: host='{host}' banco='{banco}'")

    if excecao_valida:
        print(
            f"ATENÇÃO: host '{host}' está fora da allowlist de bancos locais e foi "
            "liberado explicitamente via --permitir-host. Confirme que este banco NÃO "
            "tem dados reais de clientes/operação — o seed pode gerar milhares de "
            "registros fictícios nele."
        )
    else:
        print(
            "Atenção: este host pode ser tanto o Postgres do docker-compose quanto um "
            "Postgres nativo instalado na máquina, se ambos escutarem na mesma porta. "
            "Confirme que é o banco de desenvolvimento correto antes de prosseguir."
        )

    if confirmar_automaticamente:
        return

    if excecao_valida:
        resposta = input(f"Digite o host exatamente ('{host}') para confirmar: ").strip()
        if resposta != host:
            raise AmbienteInseguroError("Confirmação não recebida. Abortando.")
    else:
        resposta = input("Digite 'sim' para confirmar e continuar: ").strip().lower()
        if resposta != "sim":
            raise AmbienteInseguroError("Confirmação não recebida. Abortando.")
