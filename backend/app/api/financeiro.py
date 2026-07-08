from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.financeiro import (
    DespesaCreate,
    DespesaOut,
    PagamentoCreate,
    PagamentoOut,
    RentabilidadeVeiculoOut,
)
from app.services import financeiro_service

router = APIRouter(prefix="/financeiro", tags=["financeiro"])


@router.get("/pagamentos", response_model=Page[PagamentoOut])
def listar_pagamentos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    contrato_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("financeiro:visualizar")),
) -> Page[PagamentoOut]:
    itens, total = financeiro_service.listar_pagamentos(db, page, limit, contrato_id)
    data = [PagamentoOut.model_validate(p) for p in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("/pagamentos", response_model=PagamentoOut, status_code=status.HTTP_201_CREATED)
def lancar_pagamento(
    payload: PagamentoCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("financeiro:lancar")),
) -> PagamentoOut:
    return financeiro_service.lancar_pagamento(db, payload)


@router.patch("/pagamentos/{pagamento_id}/estorno", response_model=PagamentoOut)
def estornar_pagamento(
    pagamento_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("financeiro:aprovar_estorno")),
) -> PagamentoOut:
    return financeiro_service.estornar_pagamento(db, pagamento_id)


@router.get("/despesas", response_model=Page[DespesaOut])
def listar_despesas(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("financeiro:visualizar")),
) -> Page[DespesaOut]:
    itens, total = financeiro_service.listar_despesas(db, page, limit, veiculo_id)
    data = [DespesaOut.model_validate(d) for d in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("/despesas", response_model=DespesaOut, status_code=status.HTTP_201_CREATED)
def registrar_despesa(
    payload: DespesaCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("financeiro:lancar")),
) -> DespesaOut:
    return financeiro_service.registrar_despesa(db, payload)


@router.get("/rentabilidade", response_model=list[RentabilidadeVeiculoOut])
def rentabilidade(
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("financeiro:visualizar")),
) -> list[RentabilidadeVeiculoOut]:
    return financeiro_service.rentabilidade_por_veiculo(db)
