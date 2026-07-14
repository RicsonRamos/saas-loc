from collections import defaultdict
from datetime import UTC, datetime, time, timedelta
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.contrato import STATUS_CANCELADO, Contrato
from app.models.dano import Dano
from app.models.financeiro import (
    STATUS_PAGAMENTO_ESTORNADO,
    STATUS_PAGAMENTO_PAGO,
    STATUS_PAGAMENTO_PENDENTE,
    Despesa,
    Pagamento,
)
from app.models.multa import Multa
from app.models.sinistro import Sinistro
from app.models.veiculo import Veiculo
from app.schemas.dano import DanoCreate
from app.schemas.financeiro import DespesaCreate, PagamentoCreate
from app.schemas.multa import MultaCreate
from app.schemas.sinistro import SinistroCreate
from app.seed.fake import escolher, fake

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
    """Insere em lote (bypassa `multa_service.criar`, que só faz insert simples sem
    efeito colateral em outra tabela)."""
    mapa = _mapa_contratos_por_veiculo(contratos)
    hoje = datetime.now(UTC).date()
    multas: list[Multa] = []

    for _ in range(quantidade):
        veiculo = escolher(veiculos)
        contrato = escolher(mapa[veiculo.id]) if mapa.get(veiculo.id) else None
        payload = MultaCreate(
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
        )
        multas.append(Multa(**payload.model_dump()))

    db.add_all(multas)
    db.commit()
    print(f"  multas: {len(multas)} criadas")
    return len(multas)


def criar_sinistros(
    db: Session, veiculos: list[Veiculo], contratos: list[Contrato], quantidade: int
) -> int:
    """Insere em lote (bypassa `sinistro_service.criar`, que só faz insert simples sem
    efeito colateral em outra tabela)."""
    mapa = _mapa_contratos_por_veiculo(contratos)
    hoje = datetime.now(UTC).date()
    sinistros: list[Sinistro] = []

    for _ in range(quantidade):
        veiculo = escolher(veiculos)
        contrato = escolher(mapa[veiculo.id]) if mapa.get(veiculo.id) else None
        payload = SinistroCreate(
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
        )
        sinistros.append(Sinistro(**payload.model_dump()))

    db.add_all(sinistros)
    db.commit()
    print(f"  sinistros: {len(sinistros)} criados")
    return len(sinistros)


def criar_danos(
    db: Session, veiculos: list[Veiculo], contratos: list[Contrato], quantidade: int
) -> int:
    """Insere em lote (bypassa `dano_service.criar`, que só faz insert simples sem
    efeito colateral em outra tabela)."""
    mapa = _mapa_contratos_por_veiculo(contratos)
    hoje = datetime.now(UTC).date()
    danos: list[Dano] = []

    for _ in range(quantidade):
        veiculo = escolher(veiculos)
        contrato = escolher(mapa[veiculo.id]) if mapa.get(veiculo.id) else None
        payload = DanoCreate(
            veiculo_id=veiculo.id,
            cliente_id=contrato.cliente_id if contrato else None,
            contrato_id=contrato.id if contrato else None,
            tipo=escolher(["arranhao", "amassado", "quebra_vidro", "dano_interno", "outro"]),
            descricao=escolher(["Identificado na devolução", "Reportado pelo cliente", None]),
            data=hoje - timedelta(days=fake.random_int(1, 400)),
            valor_reparo=Decimal(fake.random_int(100, 3000)),
            status=escolher(["pendente", "pendente", "reparado"]),
        )
        danos.append(Dano(**payload.model_dump()))

    db.add_all(danos)
    db.commit()
    print(f"  danos: {len(danos)} criados")
    return len(danos)


def criar_despesas(db: Session, veiculos: list[Veiculo], quantidade: int) -> int:
    """Insere em lote (bypassa `financeiro_service.registrar_despesa`, que só faz
    insert simples sem efeito colateral em outra tabela)."""
    hoje = datetime.now(UTC).date()
    despesas: list[Despesa] = []

    for _ in range(quantidade):
        veiculo = escolher(veiculos) if fake.random.random() < 0.8 else None
        payload = DespesaCreate(
            veiculo_id=veiculo.id if veiculo else None,
            categoria=escolher(_CATEGORIAS_DESPESA),
            valor=Decimal(fake.random_int(50, 3000)),
            data=datetime.combine(
                hoje - timedelta(days=fake.random_int(1, 400)), time(9, 0), tzinfo=UTC
            ),
            descricao=escolher([None, "Lançamento recorrente", "Despesa avulsa"]),
        )
        despesas.append(Despesa(**payload.model_dump()))

    db.add_all(despesas)
    db.commit()
    print(f"  despesas: {len(despesas)} criadas")
    return len(despesas)


def criar_pagamentos(db: Session, contratos: list[Contrato]) -> int:
    """Insere em lote (bypassa `financeiro_service.lancar_pagamento`/
    `estornar_pagamento`, que só fazem insert/setattr simples sem efeito colateral em
    outra tabela): o status final (pago, estornado ou pendente) é decidido na hora de
    montar o objeto em vez de criar-e-depois-atualizar."""
    pagamentos: list[Pagamento] = []

    for contrato in contratos:
        if contrato.status == STATUS_CANCELADO:
            continue
        dias = max((contrato.data_fim_prevista - contrato.data_inicio).days, 1)
        valor_total = contrato.valor_diaria * dias
        r = fake.random.random()

        if r < 0.75:
            payload = PagamentoCreate(
                contrato_id=contrato.id,
                valor=valor_total,
                data=contrato.data_inicio,
                metodo=escolher(["pix", "cartao_credito", "boleto"]),
            )
            status_final = (
                STATUS_PAGAMENTO_ESTORNADO if fake.random.random() < 0.08 else STATUS_PAGAMENTO_PAGO
            )
            pagamentos.append(Pagamento(**payload.model_dump(), status=status_final))
        elif r < 0.9:
            pagamentos.append(
                Pagamento(
                    contrato_id=contrato.id,
                    valor=valor_total,
                    data=contrato.data_inicio,
                    status=STATUS_PAGAMENTO_PENDENTE,
                    metodo=escolher(["pix", "boleto"]),
                )
            )
        # ~10% dos contratos ficam deliberadamente sem nenhum pagamento lançado.

    db.add_all(pagamentos)
    db.commit()
    print(f"  pagamentos: {len(pagamentos)} criados")
    return len(pagamentos)
