from datetime import UTC, datetime, time, timedelta

from sqlalchemy.orm import Session

from app.models.pneu import POSICOES_PNEU_VALIDAS, STATUS_PNEU_TROCADO
from app.models.veiculo import Veiculo
from app.schemas.abastecimento import AbastecimentoCreate
from app.schemas.pneu import PneuCreate, PneuUpdate
from app.seed.fake import escolher, fake
from app.services import abastecimento_service, pneu_service

_MARCAS_PNEU = ["Pirelli", "Michelin", "Goodyear", "Continental", "Bridgestone"]
_POSTOS = ["Posto Ipiranga BR-101", "Shell Centro", "Petrobras Rodovia", "Posto Vila Nova"]
_COMBUSTIVEIS = ["gasolina", "etanol", "diesel"]


def criar_pneus(db: Session, veiculos: list[Veiculo]) -> int:
    hoje = datetime.now(UTC).date()
    total = 0

    for veiculo in veiculos:
        if fake.random.random() < 0.35:
            continue
        for posicao in sorted(POSICOES_PNEU_VALIDAS):
            data_instalacao = hoje - timedelta(days=fake.random_int(30, 600))
            km_instalacao = max(0, veiculo.km_atual - fake.random_int(1000, 20000))
            pneu = pneu_service.criar(
                db,
                PneuCreate(
                    veiculo_id=veiculo.id,
                    marca=escolher(_MARCAS_PNEU),
                    posicao=posicao,
                    data_instalacao=data_instalacao,
                    km_instalacao=km_instalacao,
                    vida_util_km=fake.random_int(35000, 60000),
                ),
            )
            total += 1
            if fake.random.random() < 0.15:
                pneu_service.atualizar(
                    db,
                    pneu.id,
                    PneuUpdate(
                        status=STATUS_PNEU_TROCADO,
                        data_troca=hoje - timedelta(days=fake.random_int(1, 30)),
                        km_troca=max(0, veiculo.km_atual - fake.random_int(0, 500)),
                    ),
                )

    print(f"  pneus: {total} criados")
    return total


def criar_abastecimentos(db: Session, veiculos: list[Veiculo], quantidade: int) -> int:
    hoje = datetime.now(UTC).date()
    total = 0

    for _ in range(quantidade):
        veiculo = escolher(veiculos)
        data = datetime.combine(
            hoje - timedelta(days=fake.random_int(1, 400)), time(fake.random_int(6, 21)), tzinfo=UTC
        )
        litros = fake.pyfloat(min_value=15, max_value=60, right_digits=2)
        valor_por_litro = fake.pyfloat(min_value=5.5, max_value=7.2, right_digits=2)
        km = max(0, veiculo.km_atual - fake.random_int(0, 15000))
        abastecimento_service.criar(
            db,
            AbastecimentoCreate(
                veiculo_id=veiculo.id,
                data=data,
                posto=escolher(_POSTOS),
                litros=litros,
                valor=round(litros * valor_por_litro, 2),
                km=km,
                tipo_combustivel=escolher(_COMBUSTIVEIS),
            ),
        )
        total += 1

    print(f"  abastecimentos: {total} criados")
    return total
