from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa="LEI1T23", km_atual=1000):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "HB20", "ano": 2022, "km_atual": km_atual},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def test_registrar_leitura_km_atualiza_veiculo_e_grava_historico(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="leikm1@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers)

    resp = client.post(
        "/api/v1/leituras-km",
        json={
            "veiculo_id": veiculo_id,
            "km": 1500,
            "data_leitura": "2026-07-09T10:00:00Z",
            "observacao": "Checagem mensal",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["km"] == 1500

    veiculo = client.get(f"/api/v1/veiculos/{veiculo_id}", headers=headers).json()
    assert veiculo["km_atual"] == 1500

    historico = client.get(f"/api/v1/veiculos/{veiculo_id}/historico", headers=headers).json()
    assert any(e["origem"] == "leitura_km" and e["km"] == 1500 for e in historico["eventos_km"])

    listagem = client.get(
        "/api/v1/leituras-km", params={"veiculo_id": veiculo_id}, headers=headers
    ).json()
    assert listagem["meta"]["total"] == 1


def test_leitura_km_menor_que_atual_retorna_409(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="leikm2@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="LEI2T23", km_atual=2000)

    resp = client.post(
        "/api/v1/leituras-km",
        json={
            "veiculo_id": veiculo_id,
            "km": 1000,
            "data_leitura": "2026-07-09T10:00:00Z",
        },
        headers=headers,
    )
    assert resp.status_code == 409


def test_leitura_km_sem_permissao_retorna_403(client, db_session):
    usuario = criar_usuario(db_session, role="financeiro", email="leikm3@teste.com")
    headers = auth_headers(usuario)

    # financeiro nao pode criar veiculo; usa um veiculo criado por um admin
    admin = criar_usuario(db_session, role="administrador", email="leikm3-admin@teste.com")
    admin_headers = auth_headers(admin)
    veiculo_id = _criar_veiculo(client, admin_headers, placa="LEI3T23")

    resp = client.post(
        "/api/v1/leituras-km",
        json={
            "veiculo_id": veiculo_id,
            "km": 1500,
            "data_leitura": "2026-07-09T10:00:00Z",
        },
        headers=headers,
    )
    assert resp.status_code == 403
