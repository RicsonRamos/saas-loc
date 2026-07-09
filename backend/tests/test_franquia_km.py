from datetime import UTC, datetime, timedelta

from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa="FRQ1K23"):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def _criar_cliente(client, headers, documento="99988877766"):
    resp = client.post(
        "/api/v1/clientes",
        json={"nome": "Cliente Franquia", "documento": documento},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def _criar_contrato_com_franquia(client, headers, veiculo_id, cliente_id, km_contratado_mensal=1000):
    agora = datetime.now(UTC)
    resp = client.post(
        "/api/v1/contratos",
        json={
            "cliente_id": cliente_id,
            "veiculo_id": veiculo_id,
            "data_inicio": (agora - timedelta(days=30)).isoformat(),
            "data_fim_prevista": (agora + timedelta(days=1)).isoformat(),
            "valor_diaria": "150.00",
            "km_contratado_mensal": km_contratado_mensal,
        },
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()


def test_consumo_km_normal_abaixo_de_80_por_cento(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="franquia1@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="FRQ1A23")
    cliente_id = _criar_cliente(client, headers, documento="11100022233")
    contrato = _criar_contrato_com_franquia(client, headers, veiculo_id, cliente_id)

    client.patch(f"/api/v1/veiculos/{veiculo_id}", json={"km_atual": 500}, headers=headers)

    resp = client.get(f"/api/v1/contratos/{contrato['id']}", headers=headers)
    assert resp.status_code == 200
    consumo = resp.json()["consumo_km"]
    assert consumo is not None
    assert consumo["nivel"] == "normal"


def test_consumo_km_atencao_entre_80_e_100_por_cento(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="franquia2@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="FRQ2A23")
    cliente_id = _criar_cliente(client, headers, documento="22200033344")
    contrato = _criar_contrato_com_franquia(client, headers, veiculo_id, cliente_id)

    client.patch(f"/api/v1/veiculos/{veiculo_id}", json={"km_atual": 950}, headers=headers)

    resp = client.get(f"/api/v1/contratos/{contrato['id']}", headers=headers)
    assert resp.status_code == 200
    consumo = resp.json()["consumo_km"]
    assert consumo["nivel"] == "atencao"


def test_consumo_km_critico_acima_de_100_por_cento_gera_alerta_no_dashboard(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="franquia3@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="FRQ3A23")
    cliente_id = _criar_cliente(client, headers, documento="33300044455")
    contrato = _criar_contrato_com_franquia(client, headers, veiculo_id, cliente_id)

    client.patch(f"/api/v1/veiculos/{veiculo_id}", json={"km_atual": 1300}, headers=headers)

    resp = client.get(f"/api/v1/contratos/{contrato['id']}", headers=headers)
    assert resp.status_code == 200
    consumo = resp.json()["consumo_km"]
    assert consumo["nivel"] == "critico"

    dashboard_resp = client.get("/api/v1/dashboard/resumo", headers=headers)
    assert dashboard_resp.status_code == 200
    alertas = dashboard_resp.json()["alertas"]
    assert any(
        a["tipo"] == "franquia_km_excedida" and a["prioridade"] == "critico"
        for a in alertas
    )


def test_contrato_sem_km_contratado_nao_gera_consumo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="franquia4@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="FRQ4A23")
    cliente_id = _criar_cliente(client, headers, documento="44400055566")

    contrato_resp = client.post(
        "/api/v1/contratos",
        json={
            "cliente_id": cliente_id,
            "veiculo_id": veiculo_id,
            "data_inicio": "2026-08-01T10:00:00Z",
            "data_fim_prevista": "2026-08-05T10:00:00Z",
            "valor_diaria": "150.00",
        },
        headers=headers,
    )
    assert contrato_resp.status_code == 201
    assert contrato_resp.json()["consumo_km"] is None
