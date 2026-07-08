from tests.conftest import auth_headers, criar_usuario


def test_registrar_manutencao_em_andamento_bloqueia_veiculo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "MAN1T23", "modelo": "Gol", "ano": 2020},
        headers=headers,
    ).json()

    resp = client.post(
        "/api/v1/manutencoes",
        json={
            "veiculo_id": veiculo["id"],
            "tipo": "corretiva",
            "data": "2026-07-10T09:00:00Z",
            "km": 50000,
            "custo": "350.00",
            "em_andamento": True,
        },
        headers=headers,
    )
    assert resp.status_code == 201

    veiculo_atualizado = client.get(
        f"/api/v1/veiculos/{veiculo['id']}", headers=headers
    ).json()
    assert veiculo_atualizado["status"] == "em_manutencao"
    assert veiculo_atualizado["km_atual"] == 50000


def test_tipo_de_manutencao_invalido_retorna_422(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "INV1D23", "modelo": "Gol", "ano": 2020},
        headers=headers,
    ).json()

    resp = client.post(
        "/api/v1/manutencoes",
        json={
            "veiculo_id": veiculo["id"],
            "tipo": "revisao_inexistente",
            "data": "2026-07-10T09:00:00Z",
            "km": 50000,
            "custo": "350.00",
        },
        headers=headers,
    )
    assert resp.status_code == 422
