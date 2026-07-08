import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def _serializar(valor: Any) -> Any:
    """Converte tipos não nativos de JSON (Decimal/date/datetime/UUID) para str.

    Necessário porque `dados_anteriores`/`dados_novos` são colunas JSONB e o
    psycopg não sabe serializar esses tipos Python sem essa conversão explícita.
    """
    if isinstance(valor, Decimal | date | datetime | uuid.UUID):
        return str(valor)
    return valor


def serializar_campos(campos: dict[str, Any]) -> dict[str, Any]:
    return {chave: _serializar(valor) for chave, valor in campos.items()}


def registrar_auditoria(
    db: Session,
    *,
    usuario_id: uuid.UUID | None,
    acao: str,
    entidade: str,
    entidade_id: uuid.UUID,
    dados_anteriores: dict[str, Any] | None = None,
    dados_novos: dict[str, Any] | None = None,
    ip: str | None = None,
    descricao: str | None = None,
) -> None:
    """Registra uma entrada de auditoria na mesma transação do chamador.

    Não faz `db.commit()` de propósito: o log só deve persistir se a mutação
    de negócio que o originou também persistir (mesmo commit único do service).
    """
    db.add(
        AuditLog(
            usuario_id=usuario_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            dados_anteriores=serializar_campos(dados_anteriores) if dados_anteriores else None,
            dados_novos=serializar_campos(dados_novos) if dados_novos else None,
            ip=ip,
            descricao=descricao,
        )
    )
