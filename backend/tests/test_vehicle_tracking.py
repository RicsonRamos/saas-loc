from decimal import Decimal

from app.models.vehicle_tracking import VehicleTracking
from app.models.veiculo import Veiculo


def test_vehicle_tracking_mapeado_corretamente(db_session):
    """Sem service/router nesta fase — só garante que o model está corretamente
    mapeado contra o schema criado pela migration 0009."""
    veiculo = Veiculo(placa="GPS1A23", modelo="Onix", ano=2024)
    db_session.add(veiculo)
    db_session.commit()

    registro = VehicleTracking(
        veiculo_id=veiculo.id,
        latitude=Decimal("-23.550520"),
        longitude=Decimal("-46.633308"),
        registrado_em="2026-07-08T12:00:00+00:00",
        fonte="manual",
    )
    db_session.add(registro)
    db_session.commit()
    db_session.refresh(registro)

    assert registro.id is not None
    assert registro.veiculo_id == veiculo.id
    assert registro.latitude == Decimal("-23.550520")
