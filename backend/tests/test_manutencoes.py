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


def test_atualizar_e_remover_manutencao(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin4@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "EDT1M23", "modelo": "Gol", "ano": 2020},
        headers=headers,
    ).json()

    manutencao = client.post(
        "/api/v1/manutencoes",
        json={
            "veiculo_id": veiculo["id"],
            "tipo": "preventiva",
            "data": "2026-07-10T09:00:00Z",
            "km": 40000,
            "custo": "200.00",
        },
        headers=headers,
    ).json()

    atualizar_resp = client.patch(
        f"/api/v1/manutencoes/{manutencao['id']}",
        json={"custo": "250.00", "oficina": "Oficina Central"},
        headers=headers,
    )
    assert atualizar_resp.status_code == 200
    assert atualizar_resp.json()["oficina"] == "Oficina Central"

    remover_resp = client.delete(f"/api/v1/manutencoes/{manutencao['id']}", headers=headers)
    assert remover_resp.status_code == 204

    obter_resp = client.get(f"/api/v1/manutencoes/{manutencao['id']}", headers=headers)
    assert obter_resp.status_code == 404


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
