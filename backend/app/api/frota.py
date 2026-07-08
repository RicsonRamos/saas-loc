from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.veiculo import Veiculo
from app.schemas.common import Page, PageMeta
from app.schemas.veiculo import HistoricoVeiculoOut, VeiculoCreate, VeiculoOut, VeiculoUpdate
from app.services import veiculo_service

router = APIRouter(prefix="/veiculos", tags=["frota"])


def _para_saida(veiculo: Veiculo) -> VeiculoOut:
    saida = VeiculoOut.model_validate(veiculo)
    saida.status = veiculo_service.calcular_status_efetivo(veiculo)
    return saida


@router.get("", response_model=Page[VeiculoOut])
def listar_veiculos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filtro: str | None = Query(None, alias="status"),
    busca: str | None = Query(None, description="Busca por placa, modelo ou chassi"),
    marca: str | None = None,
    categoria: str | None = None,
    ano: int | None = None,
    filial_id: str | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:visualizar")),
) -> Page[VeiculoOut]:
    itens, total = veiculo_service.listar(
        db, page, limit, status_filtro, busca, marca, categoria, ano, filial_id
    )
    data = [_para_saida(v) for v in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=VeiculoOut, status_code=status.HTTP_201_CREATED)
def criar_veiculo(
    payload: VeiculoCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:editar")),
) -> VeiculoOut:
    return _para_saida(veiculo_service.criar(db, payload))


@router.get("/{veiculo_id}", response_model=VeiculoOut)
def obter_veiculo(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:visualizar")),
) -> VeiculoOut:
    return _para_saida(veiculo_service.obter(db, veiculo_id))


@router.patch("/{veiculo_id}", response_model=VeiculoOut)
def atualizar_veiculo(
    veiculo_id: UUID,
    payload: VeiculoUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:editar")),
) -> VeiculoOut:
    return _para_saida(veiculo_service.atualizar(db, veiculo_id, payload))


@router.get("/{veiculo_id}/historico", response_model=HistoricoVeiculoOut)
def obter_historico_veiculo(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:visualizar")),
) -> HistoricoVeiculoOut:
    return veiculo_service.historico(db, veiculo_id)


@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_veiculo(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:editar")),
) -> None:
    veiculo_service.remover(db, veiculo_id)
