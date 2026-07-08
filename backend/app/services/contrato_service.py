import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.audit import registrar_auditoria
from app.exceptions import ConflictError, NotFoundError, VeiculoIndisponivelError
from app.models.cliente import Cliente
from app.models.contrato import (
    STATUS_ATIVO,
    STATUS_CANCELADO,
    STATUS_ENCERRADO,
    Contrato,
    ContratoEvento,
)
from app.models.veiculo import (
    STATUS_ALUGADO,
    STATUS_DISPONIVEL,
    STATUS_EM_MANUTENCAO,
    STATUS_INATIVO,
    Veiculo,
)
from app.schemas.contrato import ContratoCreate, ContratoDevolucao
from app.services.common import paginar


def _obter_veiculo(db: Session, veiculo_id: uuid.UUID) -> Veiculo:
    veiculo = db.get(Veiculo, veiculo_id)
    if veiculo is None or veiculo.deleted_at is not None:
        raise NotFoundError("Veículo não encontrado.")
    return veiculo


def criar_locacao(
    db: Session,
    payload: ContratoCreate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Contrato:
    """Cria o contrato/locação já como 'ativo' (reserva e contrato são o mesmo conceito).

    A prevenção de dupla alocação real vem da constraint de exclusão do banco
    (`contratos_sem_overlap`) — se duas requisições concorrentes tentarem reservar
    o mesmo veículo em período sobreposto, apenas uma delas terá o INSERT aceito.
    """
    veiculo = _obter_veiculo(db, payload.veiculo_id)
    if veiculo.status in (STATUS_EM_MANUTENCAO, STATUS_INATIVO):
        raise VeiculoIndisponivelError(
            "O veículo está em manutenção ou inativo e não pode ser alocado a uma locação."
        )

    cliente = db.get(Cliente, payload.cliente_id)
    if cliente is None or cliente.deleted_at is not None:
        raise NotFoundError("Cliente não encontrado.")

    contrato = Contrato(
        cliente_id=payload.cliente_id,
        veiculo_id=payload.veiculo_id,
        data_inicio=payload.data_inicio,
        data_fim_prevista=payload.data_fim_prevista,
        valor_diaria=payload.valor_diaria,
        km_inicio=payload.km_inicio if payload.km_inicio is not None else veiculo.km_atual,
        status=STATUS_ATIVO,
    )
    db.add(contrato)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        if "contratos_sem_overlap" in str(exc.orig):
            raise VeiculoIndisponivelError(
                "O veículo selecionado já está reservado para o período informado."
            ) from exc
        raise

    veiculo.status = STATUS_ALUGADO
    db.add(
        ContratoEvento(contrato_id=contrato.id, status_anterior=None, status_novo=STATUS_ATIVO)
    )
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="criar",
        entidade="contrato",
        entidade_id=contrato.id,
        dados_novos={"status": STATUS_ATIVO, "veiculo_id": str(contrato.veiculo_id)},
        ip=ip,
    )
    db.commit()
    db.refresh(contrato)
    return contrato


def listar(
    db: Session, page: int, limit: int, status: str | None = None
) -> tuple[list[Contrato], int]:
    stmt = select(Contrato).order_by(Contrato.created_at.desc())
    if status:
        stmt = stmt.where(Contrato.status == status)
    return paginar(db, stmt, page, limit)


def obter(db: Session, contrato_id: uuid.UUID) -> Contrato:
    contrato = db.get(Contrato, contrato_id)
    if contrato is None:
        raise NotFoundError("Contrato não encontrado.")
    return contrato


def devolver(
    db: Session,
    contrato_id: uuid.UUID,
    payload: ContratoDevolucao,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Contrato:
    contrato = obter(db, contrato_id)
    if contrato.status != STATUS_ATIVO:
        raise ConflictError("Só é possível registrar devolução de um contrato ativo.")

    status_anterior = contrato.status
    contrato.status = STATUS_ENCERRADO
    contrato.data_fim_real = payload.data_fim_real or datetime.now(UTC)

    veiculo = _obter_veiculo(db, contrato.veiculo_id)
    veiculo.status = STATUS_DISPONIVEL
    if payload.km_final is not None:
        veiculo.km_atual = payload.km_final
        contrato.km_final = payload.km_final

    db.add(
        ContratoEvento(
            contrato_id=contrato.id,
            status_anterior=status_anterior,
            status_novo=STATUS_ENCERRADO,
        )
    )
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="mudar_status",
        entidade="contrato",
        entidade_id=contrato.id,
        dados_anteriores={"status": status_anterior},
        dados_novos={"status": STATUS_ENCERRADO},
        ip=ip,
    )
    db.commit()
    db.refresh(contrato)
    return contrato


def cancelar(
    db: Session,
    contrato_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Contrato:
    contrato = obter(db, contrato_id)
    if contrato.status != STATUS_ATIVO:
        raise ConflictError("Só é possível cancelar um contrato ativo.")

    status_anterior = contrato.status
    contrato.status = STATUS_CANCELADO

    veiculo = _obter_veiculo(db, contrato.veiculo_id)
    veiculo.status = STATUS_DISPONIVEL

    db.add(
        ContratoEvento(
            contrato_id=contrato.id,
            status_anterior=status_anterior,
            status_novo=STATUS_CANCELADO,
        )
    )
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="mudar_status",
        entidade="contrato",
        entidade_id=contrato.id,
        dados_anteriores={"status": status_anterior},
        dados_novos={"status": STATUS_CANCELADO},
        ip=ip,
    )
    db.commit()
    db.refresh(contrato)
    return contrato
