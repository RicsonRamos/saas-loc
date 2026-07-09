from collections import defaultdict
from datetime import UTC, datetime, time, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.contrato import STATUS_CANCELADO, Contrato
from app.models.financeiro import STATUS_PAGAMENTO_PENDENTE, Pagamento
from app.models.veiculo import Veiculo
from app.schemas.dano import DanoCreate
from app.schemas.financeiro import DespesaCreate, PagamentoCreate
from app.schemas.multa import MultaCreate
from app.schemas.sinistro import SinistroCreate
from app.seed.fake import escolher, fake
from app.services import dano_service, financeiro_service, multa_service, sinistro_service

_INFRACOES = [
    "Excesso de velocidade",
    "Estacionamento irregular",
    "Avanço de sinal",
    "Uso indevido de celular",
]
_CATEGORIAS_DESPESA = ["ipva", "seguro", "multa_administrativa", "lavagem", "estacionamento"]


def _mapa_contratos_por_veiculo(contratos: list[Contrato]) -> dict[UUID, list[Contrato]]:
    mapa: dict[UUID, list[Contrato]] = defaultdict(list)
    for contrato in contratos:
        mapa[contrato.veiculo_id].append(contrato)
    return mapa


def criar_multas(
    db: Session, veiculos: list[Veiculo], contratos: list[Contrato], quantidade: int
) -> int:
    mapa = _mapa_contratos_por_veiculo(contratos)
    hoje = datetime.now(UTC).date()
    total = 0

    for _ in range(quantidade):
        veiculo = escolher(veiculos)
        contrato = escolher(mapa[veiculo.id]) if mapa.get(veiculo.id) else None
        multa_service.criar(
            db,
            MultaCreate(
                veiculo_id=veiculo.id,
                cliente_id=contrato.cliente_id if contrato else None,
                contrato_id=contrato.id if contrato else None,
                data=datetime.combine(
                    hoje - timedelta(days=fake.random_int(1, 400)), time(10, 0), tzinfo=UTC
                ),
                infracao=escolher(_INFRACOES),
                local=fake.street_name(),
                valor=Decimal(fake.random_int(90, 900)),
                pontos=escolher([3, 4, 5, 7]),
                status=escolher(["pendente", "pendente", "paga", "recorrida"]),
            ),
        )
        total += 1

    print(f"  multas: {total} criadas")
    return total


def criar_sinistros(
    db: Session, veiculos: list[Veiculo], contratos: list[Contrato], quantidade: int
) -> int:
    mapa = _mapa_contratos_por_veiculo(contratos)
    hoje = datetime.now(UTC).date()
    total = 0

    for _ in range(quantidade):
        veiculo = escolher(veiculos)
        contrato = escolher(mapa[veiculo.id]) if mapa.get(veiculo.id) else None
        sinistro_service.criar(
            db,
            SinistroCreate(
                veiculo_id=veiculo.id,
                cliente_id=contrato.cliente_id if contrato else None,
                contrato_id=contrato.id if contrato else None,
                tipo=escolher(["batida", "roubo", "furto", "enchente", "incendio"]),
                data=datetime.combine(
                    hoje - timedelta(days=fake.random_int(1, 500)), time(12, 0), tzinfo=UTC
                ),
                descricao=escolher(["Colisão traseira leve", "Danos em estacionamento", None]),
                valor_prejuizo=Decimal(fake.random_int(500, 15000)),
                seguradora_acionada=fake.random.random() < 0.6,
                status=escolher(["aberto", "em_andamento", "finalizado"]),
            ),
        )
        total += 1

    print(f"  sinistros: {total} criados")
    return total


def criar_danos(
    db: Session, veiculos: list[Veiculo], contratos: list[Contrato], quantidade: int
) -> int:
    mapa = _mapa_contratos_por_veiculo(contratos)
    hoje = datetime.now(UTC).date()
    total = 0

    for _ in range(quantidade):
        veiculo = escolher(veiculos)
        contrato = escolher(mapa[veiculo.id]) if mapa.get(veiculo.id) else None
        dano_service.criar(
            db,
            DanoCreate(
                veiculo_id=veiculo.id,
                cliente_id=contrato.cliente_id if contrato else None,
                contrato_id=contrato.id if contrato else None,
                tipo=escolher(["arranhao", "amassado", "quebra_vidro", "dano_interno", "outro"]),
                descricao=escolher(["Identificado na devolução", "Reportado pelo cliente", None]),
                data=hoje - timedelta(days=fake.random_int(1, 400)),
                valor_reparo=Decimal(fake.random_int(100, 3000)),
                status=escolher(["pendente", "pendente", "reparado"]),
            ),
        )
        total += 1

    print(f"  danos: {total} criados")
    return total


def criar_despesas(db: Session, veiculos: list[Veiculo], quantidade: int) -> int:
    hoje = datetime.now(UTC).date()
    total = 0

    for _ in range(quantidade):
        veiculo = escolher(veiculos) if fake.random.random() < 0.8 else None
        financeiro_service.registrar_despesa(
            db,
            DespesaCreate(
                veiculo_id=veiculo.id if veiculo else None,
                categoria=escolher(_CATEGORIAS_DESPESA),
                valor=Decimal(fake.random_int(50, 3000)),
                data=datetime.combine(
                    hoje - timedelta(days=fake.random_int(1, 400)), time(9, 0), tzinfo=UTC
                ),
                descricao=escolher([None, "Lançamento recorrente", "Despesa avulsa"]),
            ),
        )
        total += 1

    print(f"  despesas: {total} criadas")
    return total


def criar_pagamentos(db: Session, contratos: list[Contrato]) -> int:
    total = 0
    pendentes: list[Pagamento] = []

    for contrato in contratos:
        if contrato.status == STATUS_CANCELADO:
            continue
        dias = max((contrato.data_fim_prevista - contrato.data_inicio).days, 1)
        valor_total = contrato.valor_diaria * dias
        r = fake.random.random()

        if r < 0.75:
            pagamento = financeiro_service.lancar_pagamento(
                db,
                PagamentoCreate(
                    contrato_id=contrato.id,
                    valor=valor_total,
                    data=contrato.data_inicio,
                    metodo=escolher(["pix", "cartao_credito", "boleto"]),
                ),
            )
            if fake.random.random() < 0.08:
                financeiro_service.estornar_pagamento(db, pagamento.id)
            total += 1
        elif r < 0.9:
            pendentes.append(
                Pagamento(
                    contrato_id=contrato.id,
                    valor=valor_total,
                    data=contrato.data_inicio,
                    status=STATUS_PAGAMENTO_PENDENTE,
                    metodo=escolher(["pix", "boleto"]),
                )
            )
            total += 1
        # ~10% dos contratos ficam deliberadamente sem nenhum pagamento lançado.

    if pendentes:
        db.add_all(pendentes)
        db.commit()

    print(f"  pagamentos: {total} criados")
    return total
