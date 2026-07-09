import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import registrar_auditoria
from app.exceptions import ConflictError, NotFoundError
from app.models.leitura_km import LeituraKm
from app.models.veiculo import Veiculo
from app.schemas.leitura_km import LeituraKmCreate
from app.services.common import paginar


def _obter_veiculo(db: Session, veiculo_id: uuid.UUID) -> Veiculo:
    veiculo = db.get(Veiculo, veiculo_id)
    if veiculo is None or veiculo.deleted_at is not None:
        raise NotFoundError("Veículo não encontrado.")
    return veiculo


def registrar(
    db: Session,
    payload: LeituraKmCreate,
    usuario_id: uuid.UUID,
    ip: str | None = None,
) -> LeituraKm:
    veiculo = _obter_veiculo(db, payload.veiculo_id)
    if payload.km < veiculo.km_atual:
        raise ConflictError(
            f"A quilometragem informada ({payload.km} km) é menor que a atual do "
            f"veículo ({veiculo.km_atual} km)."
        )

    leitura = LeituraKm(
        veiculo_id=payload.veiculo_id,
        usuario_id=usuario_id,
        km=payload.km,
        data_leitura=payload.data_leitura,
        observacao=payload.observacao,
    )
    db.add(leitura)
    veiculo.km_atual = payload.km
    db.flush()
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="criar",
        entidade="leitura_km",
        entidade_id=leitura.id,
        dados_novos={"veiculo_id": str(payload.veiculo_id), "km": payload.km},
        ip=ip,
    )
    db.commit()
    db.refresh(leitura)
    return leitura


def listar(
    db: Session, page: int, limit: int, veiculo_id: uuid.UUID | None = None
) -> tuple[list[LeituraKm], int]:
    stmt = (
        select(LeituraKm)
        .where(LeituraKm.deleted_at.is_(None))
        .order_by(LeituraKm.data_leitura.desc())
    )
    if veiculo_id:
        stmt = stmt.where(LeituraKm.veiculo_id == veiculo_id)
    return paginar(db, stmt, page, limit)
