import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.audit import registrar_auditoria
from app.exceptions import ConflictError, NotFoundError
from app.models.checklist import TIPO_DEVOLUCAO, TIPO_ENTREGA, Assinatura, Checklist, ChecklistItem
from app.models.contrato import STATUS_ATIVO, Contrato
from app.schemas.checklist import AssinaturaCreate, ChecklistCreate
from app.services import attachment_service
from app.services.common import paginar


def _obter_contrato(db: Session, contrato_id: uuid.UUID) -> Contrato:
    contrato = db.get(Contrato, contrato_id)
    if contrato is None:
        raise NotFoundError("Contrato não encontrado.")
    return contrato


def _validar_pode_criar(db: Session, contrato: Contrato, tipo: str) -> None:
    if contrato.status != STATUS_ATIVO:
        raise ConflictError("Só é possível registrar checklist enquanto o contrato está ativo.")
    if tipo == TIPO_DEVOLUCAO:
        entrega = db.scalar(
            select(Checklist).where(
                Checklist.contrato_id == contrato.id,
                Checklist.tipo == TIPO_ENTREGA,
                Checklist.deleted_at.is_(None),
            )
        )
        if entrega is None:
            raise ConflictError(
                "É necessário registrar o checklist de entrega antes do checklist de devolução."
            )


def criar(
    db: Session,
    payload: ChecklistCreate,
    usuario_id: uuid.UUID,
    ip: str | None = None,
) -> tuple[Checklist, list[ChecklistItem]]:
    contrato = _obter_contrato(db, payload.contrato_id)
    _validar_pode_criar(db, contrato, payload.tipo)

    checklist = Checklist(
        contrato_id=payload.contrato_id,
        tipo=payload.tipo,
        data=payload.data,
        usuario_id=usuario_id,
        km=payload.km,
        combustivel=payload.combustivel,
        observacoes_gerais=payload.observacoes_gerais,
    )
    db.add(checklist)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        if "uq_checklists_contrato_tipo_ativo" in str(exc.orig):
            raise ConflictError(
                f"Já existe um checklist de {payload.tipo} registrado para este contrato."
            ) from exc
        raise

    itens = [
        ChecklistItem(
            checklist_id=checklist.id,
            item=item_payload.item,
            situacao=item_payload.situacao,
            observacao=item_payload.observacao,
            foto_attachment_id=item_payload.foto_attachment_id,
        )
        for item_payload in payload.itens
    ]
    db.add_all(itens)

    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="criar",
        entidade="checklist",
        entidade_id=checklist.id,
        dados_novos={"contrato_id": str(contrato.id), "tipo": payload.tipo, "km": payload.km},
        ip=ip,
    )
    db.commit()
    db.refresh(checklist)
    return checklist, itens


def itens_do_checklist(db: Session, checklist_id: uuid.UUID) -> list[ChecklistItem]:
    return list(
        db.scalars(
            select(ChecklistItem).where(ChecklistItem.checklist_id == checklist_id)
        ).all()
    )


def obter(db: Session, checklist_id: uuid.UUID) -> tuple[Checklist, list[ChecklistItem]]:
    checklist = db.get(Checklist, checklist_id)
    if checklist is None or checklist.deleted_at is not None:
        raise NotFoundError("Checklist não encontrado.")
    return checklist, itens_do_checklist(db, checklist_id)


def listar(
    db: Session, page: int, limit: int, contrato_id: uuid.UUID | None = None
) -> tuple[list[Checklist], int]:
    stmt = (
        select(Checklist).where(Checklist.deleted_at.is_(None)).order_by(Checklist.data.desc())
    )
    if contrato_id:
        stmt = stmt.where(Checklist.contrato_id == contrato_id)
    return paginar(db, stmt, page, limit)


def comparacao(db: Session, contrato_id: uuid.UUID) -> dict:
    _obter_contrato(db, contrato_id)

    entrega = db.scalar(
        select(Checklist).where(
            Checklist.contrato_id == contrato_id,
            Checklist.tipo == TIPO_ENTREGA,
            Checklist.deleted_at.is_(None),
        )
    )
    if entrega is None:
        raise ConflictError("Checklist de entrega ainda não registrado para este contrato.")

    devolucao = db.scalar(
        select(Checklist).where(
            Checklist.contrato_id == contrato_id,
            Checklist.tipo == TIPO_DEVOLUCAO,
            Checklist.deleted_at.is_(None),
        )
    )
    if devolucao is None:
        raise ConflictError("Checklist de devolução ainda não registrado para este contrato.")

    itens_entrega = {i.item: i.situacao for i in itens_do_checklist(db, entrega.id)}
    itens_devolucao = {i.item: i.situacao for i in itens_do_checklist(db, devolucao.id)}

    todos_itens = sorted(set(itens_entrega) | set(itens_devolucao))
    comparacao_itens = [
        {
            "item": item,
            "situacao_entrega": itens_entrega.get(item),
            "situacao_devolucao": itens_devolucao.get(item),
            "mudou": itens_entrega.get(item) != itens_devolucao.get(item),
        }
        for item in todos_itens
    ]

    return {
        "checklist_entrega_id": entrega.id,
        "checklist_devolucao_id": devolucao.id,
        "itens": comparacao_itens,
    }


def atualizar_foto_item(
    db: Session,
    checklist_id: uuid.UUID,
    item_id: uuid.UUID,
    foto_attachment_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> ChecklistItem:
    item = db.get(ChecklistItem, item_id)
    if item is None or item.deleted_at is not None or item.checklist_id != checklist_id:
        raise NotFoundError("Item de checklist não encontrado.")
    attachment_service.obter(db, foto_attachment_id)

    item.foto_attachment_id = foto_attachment_id
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="atualizar",
        entidade="checklist_item",
        entidade_id=item.id,
        dados_novos={"foto_attachment_id": str(foto_attachment_id)},
        ip=ip,
    )
    db.commit()
    db.refresh(item)
    return item


def criar_assinatura(
    db: Session,
    checklist_id: uuid.UUID,
    payload: AssinaturaCreate,
    usuario_id: uuid.UUID,
    ip: str | None = None,
) -> Assinatura:
    checklist, _ = obter(db, checklist_id)
    attachment_service.obter(db, payload.attachment_id)

    assinatura = Assinatura(
        checklist_id=checklist.id,
        attachment_id=payload.attachment_id,
        usuario_id=usuario_id,
        responsavel_nome=payload.responsavel_nome,
    )
    db.add(assinatura)
    db.flush()
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="criar",
        entidade="assinatura",
        entidade_id=assinatura.id,
        dados_novos={
            "checklist_id": str(checklist.id),
            "responsavel_nome": payload.responsavel_nome,
        },
        ip=ip,
    )
    db.commit()
    db.refresh(assinatura)
    return assinatura


def remover(
    db: Session,
    checklist_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> None:
    checklist, itens = obter(db, checklist_id)
    agora = datetime.now(UTC)
    checklist.deleted_at = agora
    for item in itens:
        item.deleted_at = agora
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="excluir",
        entidade="checklist",
        entidade_id=checklist.id,
        ip=ip,
    )
    db.commit()
