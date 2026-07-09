from datetime import UTC, date, datetime, time, timedelta

from sqlalchemy.orm import Session

from app.models.leitura_km import LeituraKm
from app.models.usuario import Usuario
from app.models.vehicle_tracking import VehicleTracking
from app.models.veiculo import STATUS_ALUGADO, Veiculo
from app.seed.fake import escolher, fake

_LOTE_COMMIT = 500


def _km_interpolado(km_base: int, km_alvo: int, entrada: date, hoje: date, na_data: date) -> int:
    dias_totais = max((hoje - entrada).days, 1)
    fracao = min(max((na_data - entrada).days / dias_totais, 0.0), 1.0)
    return km_base + round((km_alvo - km_base) * fracao)


def criar_leituras_km(db: Session, veiculos: list[Veiculo], usuarios: list[Usuario]) -> int:
    hoje = datetime.now(UTC).date()
    lote: list[LeituraKm] = []
    total = 0

    for veiculo in veiculos:
        entrada = veiculo.data_entrada_frota or (hoje - timedelta(days=180))
        km_base = veiculo.km_inicial or 0
        km_alvo = veiculo.km_atual

        cursor = entrada + timedelta(days=fake.random_int(5, 20))
        while cursor < hoje:
            km = _km_interpolado(km_base, km_alvo, entrada, hoje, cursor)
            lote.append(
                LeituraKm(
                    veiculo_id=veiculo.id,
                    usuario_id=escolher(usuarios).id,
                    km=km,
                    data_leitura=datetime.combine(cursor, time(8, 30), tzinfo=UTC),
                    observacao=escolher(
                        [None, None, None, "Checagem periódica", "Registrado na devolução"]
                    ),
                )
            )
            total += 1
            cursor += timedelta(days=fake.random_int(15, 45))

        if len(lote) >= _LOTE_COMMIT:
            db.add_all(lote)
            db.commit()
            lote = []

    if lote:
        db.add_all(lote)
        db.commit()

    print(f"  leituras_km: {total} criadas")
    return total


def criar_vehicle_tracking(db: Session, veiculos: list[Veiculo]) -> int:
    """Pontos de GPS fictícios só para veículos "alugados" — placeholder para a
    futura integração (ver app/models/vehicle_tracking.py), sem service/tela ainda."""
    hoje = datetime.now(UTC)
    lote: list[VehicleTracking] = []
    alugados = [v for v in veiculos if v.status == STATUS_ALUGADO]

    for veiculo in alugados:
        lat_base = fake.pyfloat(min_value=-23.7, max_value=-23.4)
        lon_base = fake.pyfloat(min_value=-46.8, max_value=-46.4)
        for i in range(fake.random_int(2, 6)):
            lote.append(
                VehicleTracking(
                    veiculo_id=veiculo.id,
                    latitude=round(lat_base + fake.pyfloat(min_value=-0.05, max_value=0.05), 6),
                    longitude=round(lon_base + fake.pyfloat(min_value=-0.05, max_value=0.05), 6),
                    registrado_em=hoje - timedelta(hours=i * fake.random_int(2, 10)),
                    fonte="seed",
                )
            )

    if lote:
        db.add_all(lote)
        db.commit()
    print(f"  vehicle_tracking: {len(lote)} criados")
    return len(lote)
