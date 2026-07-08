"""Rota pública de consulta do veículo via QR code.

ATENÇÃO: este router é registrado em `router.py` sem `Depends(require_permission)`
de propósito — é o único endpoint da API sem autenticação. Não adicionar guard
aqui sem também atualizar a página pública correspondente no frontend.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.veiculo_publico import LocacaoPublicaOut, VeiculoPublicoOut
from app.services import veiculo_service

router = APIRouter(prefix="/veiculo/public", tags=["veiculo-publico"])


@router.get("/{codigo}", response_model=VeiculoPublicoOut)
def consultar_veiculo_publico(codigo: str, db: Session = Depends(get_db)) -> VeiculoPublicoOut:
    veiculo = veiculo_service.obter_por_codigo_publico(db, codigo)
    contrato_ativo = veiculo_service.contrato_ativo_do_veiculo(db, veiculo.id)

    return VeiculoPublicoOut(
        placa=veiculo.placa,
        modelo=veiculo.modelo,
        marca=veiculo.marca,
        ano=veiculo.ano,
        status=veiculo_service.calcular_status_efetivo(veiculo),
        km_atual=veiculo.km_atual,
        locacao_atual=LocacaoPublicaOut(
            em_uso=True, data_fim_prevista=contrato_ativo.data_fim_prevista
        )
        if contrato_ativo
        else LocacaoPublicaOut(em_uso=False),
    )
