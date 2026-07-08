from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.usuario import Usuario
from app.models.veiculo import Veiculo
from app.schemas.common import Page, PageMeta
from app.schemas.veiculo import HistoricoVeiculoOut, VeiculoCreate, VeiculoOut, VeiculoUpdate
from app.services import abastecimento_service, manutencao_service, pdf_service, veiculo_service


def _ip_do_cliente(request: Request) -> str | None:
    return request.client.host if request.client else None

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
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:editar")),
) -> VeiculoOut:
    return _para_saida(
        veiculo_service.criar(db, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request))
    )


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
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:editar")),
) -> VeiculoOut:
    return _para_saida(
        veiculo_service.atualizar(
            db, veiculo_id, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
        )
    )


@router.get("/{veiculo_id}/historico", response_model=HistoricoVeiculoOut)
def obter_historico_veiculo(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:visualizar")),
) -> HistoricoVeiculoOut:
    return veiculo_service.historico(db, veiculo_id)


def _resposta_pdf(conteudo: bytes, nome_arquivo: str) -> Response:
    return Response(
        content=conteudo,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{nome_arquivo}"'},
    )


@router.get("/{veiculo_id}/ficha.pdf")
def gerar_ficha_pdf(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:visualizar")),
) -> Response:
    veiculo = veiculo_service.obter(db, veiculo_id)
    ultimos_abastecimentos, _ = abastecimento_service.listar(
        db, page=1, limit=10, veiculo_id=veiculo_id
    )
    pdf = pdf_service.gerar_ficha_veiculo(veiculo, ultimos_abastecimentos, usuario)
    return _resposta_pdf(pdf, f"ficha-{veiculo.placa}.pdf")


@router.get("/{veiculo_id}/historico.pdf")
def gerar_historico_pdf(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:visualizar")),
) -> Response:
    veiculo = veiculo_service.obter(db, veiculo_id)
    historico = veiculo_service.historico(db, veiculo_id)
    pdf = pdf_service.gerar_historico_veiculo(veiculo, historico, usuario)
    return _resposta_pdf(pdf, f"historico-{veiculo.placa}.pdf")


@router.get("/{veiculo_id}/abastecimentos.pdf")
def gerar_abastecimentos_pdf(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:visualizar")),
) -> Response:
    veiculo = veiculo_service.obter(db, veiculo_id)
    abastecimentos, _ = abastecimento_service.listar(db, page=1, limit=1000, veiculo_id=veiculo_id)
    pdf = pdf_service.gerar_abastecimentos_veiculo(veiculo, abastecimentos, usuario)
    return _resposta_pdf(pdf, f"abastecimentos-{veiculo.placa}.pdf")


@router.get("/{veiculo_id}/manutencoes.pdf")
def gerar_manutencoes_pdf(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:visualizar")),
) -> Response:
    veiculo = veiculo_service.obter(db, veiculo_id)
    manutencoes, _ = manutencao_service.listar(db, page=1, limit=1000, veiculo_id=veiculo_id)
    pdf = pdf_service.gerar_manutencoes_veiculo(veiculo, manutencoes, usuario)
    return _resposta_pdf(pdf, f"manutencoes-{veiculo.placa}.pdf")


@router.post("/{veiculo_id}/regenerar-codigo-publico", response_model=VeiculoOut)
def regenerar_codigo_publico(
    veiculo_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:regenerar_codigo_publico")),
) -> VeiculoOut:
    return _para_saida(
        veiculo_service.regenerar_codigo_publico(
            db, veiculo_id, usuario_id=usuario.id, ip=_ip_do_cliente(request)
        )
    )


@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_veiculo(
    veiculo_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:editar")),
) -> None:
    veiculo_service.remover(db, veiculo_id, usuario_id=usuario.id, ip=_ip_do_cliente(request))
