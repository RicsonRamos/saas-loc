"""Checklists de entrega/devolução — precisam ser criados enquanto o contrato ainda
está "ativo" (mesma regra do frontend real: o botão de checklist de devolução só
aparece antes de clicar em "Devolver"), então são chamados pela fase de contratos
no momento certo, não como uma fase isolada depois.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.checklist import ITENS_CHECKLIST_VALIDOS, TIPO_DEVOLUCAO, TIPO_ENTREGA, Checklist
from app.models.contrato import Contrato
from app.models.usuario import Usuario
from app.schemas.checklist import AssinaturaCreate, ChecklistCreate, ChecklistItemCreate
from app.seed.fake import escolher, fake
from app.services import attachment_service, checklist_service

# PNG 1x1 válido (mesmo usado em backend/tests/test_checklists.py) — evita depender
# de arquivos externos para o upload fictício.
PNG_FICTICIO = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
    "890000000a49444154789c6360000002000100ffff03000006000557bf"
    "abd4000000004945454e44ae426082"
)

_ITENS_ORDENADOS = sorted(ITENS_CHECKLIST_VALIDOS)


def _gerar_itens(com_avarias: bool) -> list[ChecklistItemCreate]:
    itens = []
    for item in _ITENS_ORDENADOS:
        if com_avarias and fake.random.random() < 0.2:
            situacao = escolher(["avaria", "faltante"])
        else:
            situacao = "ok"
        itens.append(
            ChecklistItemCreate(
                item=item,
                situacao=situacao,
                observacao="Registrado no seed de desenvolvimento" if situacao != "ok" else None,
            )
        )
    return itens


def _anexar_fotos(
    db: Session, checklist_id: UUID, itens, usuario_id: UUID
) -> None:
    for item in itens:
        if item.situacao == "ok" or fake.random.random() >= 0.6:
            continue
        attachment = attachment_service.criar(
            db,
            entidade_tipo="checklist_item",
            entidade_id=item.id,
            nome_original=f"{item.item}.png",
            conteudo=PNG_FICTICIO,
            usuario_id=usuario_id,
        )
        checklist_service.atualizar_foto_item(
            db, checklist_id, item.id, attachment.id, usuario_id=usuario_id
        )


def _criar_checklist(
    db: Session,
    contrato: Contrato,
    tipo: str,
    data: datetime,
    km: int,
    usuarios: list[Usuario],
    com_uploads: bool,
) -> Checklist:
    usuario = escolher(usuarios)
    com_avarias = tipo == TIPO_DEVOLUCAO and fake.random.random() < 0.4
    checklist, itens = checklist_service.criar(
        db,
        ChecklistCreate(
            contrato_id=contrato.id,
            tipo=tipo,
            data=data,
            km=km,
            combustivel=escolher(["vazio", "1/4", "1/2", "3/4", "cheio"]),
            observacoes_gerais=escolher([None, "Veículo entregue em boas condições", None]),
            itens=_gerar_itens(com_avarias),
        ),
        usuario_id=usuario.id,
    )

    if com_uploads:
        _anexar_fotos(db, checklist.id, itens, usuario.id)
        assinatura_png = attachment_service.criar(
            db,
            entidade_tipo="assinatura",
            entidade_id=checklist.id,
            nome_original="assinatura.png",
            conteudo=PNG_FICTICIO,
            usuario_id=usuario.id,
        )
        checklist_service.criar_assinatura(
            db,
            checklist.id,
            AssinaturaCreate(
                attachment_id=assinatura_png.id,
                responsavel_nome=fake.name(),
            ),
            usuario_id=usuario.id,
        )

    return checklist


def criar_checklist_entrega(
    db: Session, contrato: Contrato, km: int, usuarios: list[Usuario], com_uploads: bool
) -> Checklist:
    return _criar_checklist(
        db, contrato, TIPO_ENTREGA, contrato.data_inicio, km, usuarios, com_uploads
    )


def criar_checklist_devolucao(
    db: Session,
    contrato: Contrato,
    km: int,
    data: datetime,
    usuarios: list[Usuario],
    com_uploads: bool,
) -> Checklist:
    return _criar_checklist(db, contrato, TIPO_DEVOLUCAO, data, km, usuarios, com_uploads)
