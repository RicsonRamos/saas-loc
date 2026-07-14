from datetime import UTC, datetime, time, timedelta

from sqlalchemy.orm import Session

from app.models.abastecimento import Abastecimento
from app.models.pneu import POSICOES_PNEU_VALIDAS, STATUS_PNEU_TROCADO, Pneu
from app.models.veiculo import Veiculo
from app.schemas.abastecimento import AbastecimentoCreate
from app.schemas.pneu import PneuCreate
from app.seed.fake import escolher, fake

_MARCAS_PNEU = ["Pirelli", "Michelin", "Goodyear", "Continental", "Bridgestone"]
_POSTOS = ["Posto Ipiranga BR-101", "Shell Centro", "Petrobras Rodovia", "Posto Vila Nova"]
_COMBUSTIVEIS = ["gasolina", "etanol", "diesel"]


def criar_pneus(db: Session, veiculos: list[Veiculo]) -> int:
    """Insere os pneus em lote (bypassa `pneu_service.criar`/`atualizar`, que só fazem
    insert/setattr simples sem efeito colateral em outra tabela — ver
    docs/10-SEED-DESENVOLVIMENTO.md). A "troca" (~15% dos pneus) é decidida direto no
    estado final do objeto em vez de criar-e-depois-atualizar."""
    hoje = datetime.now(UTC).date()
    pneus: list[Pneu] = []

    for veiculo in veiculos:
        if fake.random.random() < 0.35:
            continue
        for posicao in sorted(POSICOES_PNEU_VALIDAS):
            data_instalacao = hoje - timedelta(days=fake.random_int(30, 600))
            km_instalacao = max(0, veiculo.km_atual - fake.random_int(1000, 20000))
            payload = PneuCreate(
                veiculo_id=veiculo.id,
                marca=escolher(_MARCAS_PNEU),
                posicao=posicao,
                data_instalacao=data_instalacao,
                km_instalacao=km_instalacao,
                vida_util_km=fake.random_int(35000, 60000),
            )
            pneu = Pneu(**payload.model_dump())
            if fake.random.random() < 0.15:
                pneu.status = STATUS_PNEU_TROCADO
                pneu.data_troca = hoje - timedelta(days=fake.random_int(1, 30))
                pneu.km_troca = max(0, veiculo.km_atual - fake.random_int(0, 500))
            pneus.append(pneu)

    db.add_all(pneus)
    db.commit()
    print(f"  pneus: {len(pneus)} criados")
    return len(pneus)


def criar_abastecimentos(db: Session, veiculos: list[Veiculo], quantidade: int) -> int:
    """Insere os abastecimentos em lote (bypassa `abastecimento_service.criar`, que só
    faz um insert simples sem efeito colateral em outra tabela)."""
    hoje = datetime.now(UTC).date()
    abastecimentos: list[Abastecimento] = []

    for _ in range(quantidade):
        veiculo = escolher(veiculos)
        data = datetime.combine(
            hoje - timedelta(days=fake.random_int(1, 400)), time(fake.random_int(6, 21)), tzinfo=UTC
        )
        litros = fake.pyfloat(min_value=15, max_value=60, right_digits=2)
        valor_por_litro = fake.pyfloat(min_value=5.5, max_value=7.2, right_digits=2)
        km = max(0, veiculo.km_atual - fake.random_int(0, 15000))
        payload = AbastecimentoCreate(
            veiculo_id=veiculo.id,
            data=data,
            posto=escolher(_POSTOS),
            litros=litros,
            valor=round(litros * valor_por_litro, 2),
            km=km,
            tipo_combustivel=escolher(_COMBUSTIVEIS),
        )
        abastecimentos.append(Abastecimento(**payload.model_dump()))

    db.add_all(abastecimentos)
    db.commit()
    print(f"  abastecimentos: {len(abastecimentos)} criados")
    return len(abastecimentos)
