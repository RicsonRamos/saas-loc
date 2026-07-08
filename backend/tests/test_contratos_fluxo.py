from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa="XYZ9A87"):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "HB20", "ano": 2022},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def _criar_cliente(client, headers, documento="12345678900"):
    resp = client.post(
        "/api/v1/clientes",
        json={"nome": "Cliente Teste", "documento": documento},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def test_fluxo_completo_locacao_devolucao_libera_veiculo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers)
    cliente_id = _criar_cliente(client, headers)

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
    contrato = contrato_resp.json()
    assert contrato["status"] == "ativo"

    veiculo = client.get(f"/api/v1/veiculos/{veiculo_id}", headers=headers).json()
    assert veiculo["status"] == "alugado"

    devolucao_resp = client.patch(
        f"/api/v1/contratos/{contrato['id']}/devolucao",
        json={"km_final": 15000},
        headers=headers,
    )
    assert devolucao_resp.status_code == 200
    assert devolucao_resp.json()["status"] == "encerrado"

    veiculo = client.get(f"/api/v1/veiculos/{veiculo_id}", headers=headers).json()
    assert veiculo["status"] == "disponivel"
    assert veiculo["km_atual"] == 15000


def test_cancelamento_libera_veiculo_para_nova_locacao(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="CAN1C23")
    cliente_id = _criar_cliente(client, headers, documento="11122233344")

    contrato = client.post(
        "/api/v1/contratos",
        json={
            "cliente_id": cliente_id,
            "veiculo_id": veiculo_id,
            "data_inicio": "2026-08-01T10:00:00Z",
            "data_fim_prevista": "2026-08-05T10:00:00Z",
            "valor_diaria": "150.00",
        },
        headers=headers,
    ).json()

    cancelamento_resp = client.patch(
        f"/api/v1/contratos/{contrato['id']}/cancelamento", headers=headers
    )
    assert cancelamento_resp.status_code == 200
    assert cancelamento_resp.json()["status"] == "cancelado"

    novo_contrato_resp = client.post(
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
    assert novo_contrato_resp.status_code == 201


def test_criar_contrato_com_veiculo_em_manutencao_retorna_409(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="MNT1C23")
    client.patch(
        f"/api/v1/veiculos/{veiculo_id}",
        json={"status": "em_manutencao"},
        headers=headers,
    )
    cliente_id = _criar_cliente(client, headers, documento="55566677788")

    resp = client.post(
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
    assert resp.status_code == 409
