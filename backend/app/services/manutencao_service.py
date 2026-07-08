import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.manutencao import Manutencao
from app.models.veiculo import STATUS_EM_MANUTENCAO, Veiculo
from app.schemas.manutencao import ManutencaoCreate
from app.services.common import paginar


def registrar(db: Session, payload: ManutencaoCreate) -> Manutencao:
    veiculo = db.get(Veiculo, payload.veiculo_id)
    if veiculo is None or veiculo.deleted_at is not None:
        raise NotFoundError("Veículo não encontrado.")

    dados = payload.model_dump(exclude={"em_andamento"})
    manutencao = Manutencao(**dados)
    db.add(manutencao)

    if payload.km > veiculo.km_atual:
        veiculo.km_atual = payload.km
    if payload.em_andamento:
        veiculo.status = STATUS_EM_MANUTENCAO

    db.commit()
    db.refresh(manutencao)
    return manutencao


def listar(
    db: Session, page: int, limit: int, veiculo_id: uuid.UUID | None = None
) -> tuple[list[Manutencao], int]:
    stmt = select(Manutencao).order_by(Manutencao.data.desc())
    if veiculo_id:
        stmt = stmt.where(Manutencao.veiculo_id == veiculo_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, manutencao_id: uuid.UUID) -> Manutencao:
    manutencao = db.get(Manutencao, manutencao_id)
    if manutencao is None:
        raise NotFoundError("Registro de manutenção não encontrado.")
    return manutencao
