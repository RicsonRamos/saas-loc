import uuid
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import registrar_auditoria, serializar_campos
from app.exceptions import NotFoundError
from app.models.plano_manutencao import PlanoManutencao
from app.models.veiculo import Veiculo
from app.schemas.plano_manutencao import (
    PlanoManutencaoCreate,
    PlanoManutencaoOut,
    PlanoManutencaoUpdate,
)
from app.services.common import paginar

NIVEL_NORMAL = "normal"
NIVEL_ATENCAO = "atencao"
NIVEL_CRITICO = "critico"

LIMIAR_ATENCAO = 0.8


def _obter_veiculo(db: Session, veiculo_id: uuid.UUID) -> Veiculo:
    veiculo = db.get(Veiculo, veiculo_id)
    if veiculo is None or veiculo.deleted_at is not None:
        raise NotFoundError("Veículo não encontrado.")
    return veiculo


def calcular_status(
    plano: PlanoManutencao, veiculo: Veiculo, hoje: date | None = None
) -> tuple[str, int | None, int | None]:
    """Calcula a prioridade do plano e quanto falta (km e/ou dias) para o próximo vencimento."""
    hoje = hoje or datetime.now(UTC).date()

    faltam_km: int | None = None
    nivel_km = NIVEL_NORMAL
    if plano.intervalo_km is not None:
        base_km = plano.ultima_execucao_km or 0
        faltam_km = base_km + plano.intervalo_km - veiculo.km_atual
        percentual = 1 - (faltam_km / plano.intervalo_km)
        if faltam_km <= 0:
            nivel_km = NIVEL_CRITICO
        elif percentual >= LIMIAR_ATENCAO:
            nivel_km = NIVEL_ATENCAO

    faltam_dias: int | None = None
    nivel_dias = NIVEL_NORMAL
    if plano.intervalo_dias is not None:
        base_data = plano.ultima_execucao_data or hoje
        proxima_data = base_data + timedelta(days=plano.intervalo_dias)
        faltam_dias = (proxima_data - hoje).days
        percentual = 1 - (faltam_dias / plano.intervalo_dias)
        if faltam_dias <= 0:
            nivel_dias = NIVEL_CRITICO
        elif percentual >= LIMIAR_ATENCAO:
            nivel_dias = NIVEL_ATENCAO

    ordem = {NIVEL_NORMAL: 0, NIVEL_ATENCAO: 1, NIVEL_CRITICO: 2}
    prioridade = max((nivel_km, nivel_dias), key=lambda n: ordem[n])
    return prioridade, faltam_km, faltam_dias


def para_saida_com_status(plano: PlanoManutencao, veiculo: Veiculo) -> PlanoManutencaoOut:
    prioridade, faltam_km, faltam_dias = calcular_status(plano, veiculo)
    saida = PlanoManutencaoOut.model_validate(plano)
    saida.prioridade = prioridade
    saida.faltam_km = faltam_km
    saida.faltam_dias = faltam_dias
    return saida


def criar(
    db: Session,
    payload: PlanoManutencaoCreate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> PlanoManutencao:
    _obter_veiculo(db, payload.veiculo_id)
    plano = PlanoManutencao(**payload.model_dump())
    db.add(plano)
    db.flush()
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="criar",
        entidade="plano_manutencao",
        entidade_id=plano.id,
        dados_novos=serializar_campos(payload.model_dump()),
        ip=ip,
    )
    db.commit()
    db.refresh(plano)
    return plano


def listar(
    db: Session, page: int, limit: int, veiculo_id: uuid.UUID | None = None
) -> tuple[list[PlanoManutencao], int]:
    stmt = (
        select(PlanoManutencao)
        .where(PlanoManutencao.deleted_at.is_(None))
        .order_by(PlanoManutencao.created_at.desc())
    )
    if veiculo_id:
        stmt = stmt.where(PlanoManutencao.veiculo_id == veiculo_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, plano_id: uuid.UUID) -> PlanoManutencao:
    plano = db.get(PlanoManutencao, plano_id)
    if plano is None or plano.deleted_at is not None:
        raise NotFoundError("Plano de manutenção não encontrado.")
    return plano


def atualizar(
    db: Session,
    plano_id: uuid.UUID,
    payload: PlanoManutencaoUpdate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> PlanoManutencao:
    plano = obter(db, plano_id)
    campos_alterados = payload.model_dump(exclude_unset=True)
    dados_anteriores = {campo: getattr(plano, campo) for campo in campos_alterados}
    for campo, valor in campos_alterados.items():
        setattr(plano, campo, valor)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="atualizar",
        entidade="plano_manutencao",
        entidade_id=plano.id,
        dados_anteriores=serializar_campos(dados_anteriores),
        dados_novos=serializar_campos(campos_alterados),
        ip=ip,
    )
    db.commit()
    db.refresh(plano)
    return plano


def remover(
    db: Session,
    plano_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> None:
    plano = obter(db, plano_id)
    plano.deleted_at = datetime.now(UTC)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="excluir",
        entidade="plano_manutencao",
        entidade_id=plano.id,
        ip=ip,
    )
    db.commit()
