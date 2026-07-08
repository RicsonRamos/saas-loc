from tests.conftest import auth_headers, criar_usuario


def test_criar_condutor_vinculado_a_cliente(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_mot1@teste.com")
    headers = auth_headers(usuario)

    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Empresa XPTO", "documento": "11222333000144"},
        headers=headers,
    ).json()

    resp = client.post(
        "/api/v1/motoristas",
        json={
            "nome": "Funcionário Autorizado",
            "cnh": "99988877766",
            "validade_cnh": "2027-01-01",
            "cliente_id": cliente["id"],
            "parentesco": "Funcionário autorizado",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    condutor = resp.json()
    assert condutor["cliente_id"] == cliente["id"]
    assert condutor["parentesco"] == "Funcionário autorizado"


def test_filtrar_motoristas_por_cliente_id(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_mot2@teste.com")
    headers = auth_headers(usuario)

    cliente_a = client.post(
        "/api/v1/clientes", json={"nome": "Cliente A", "documento": "22233344455"}, headers=headers
    ).json()
    cliente_b = client.post(
        "/api/v1/clientes", json={"nome": "Cliente B", "documento": "33344455566"}, headers=headers
    ).json()

    client.post(
        "/api/v1/motoristas",
        json={
            "nome": "Condutor A",
            "cnh": "11111111111",
            "validade_cnh": "2027-01-01",
            "cliente_id": cliente_a["id"],
        },
        headers=headers,
    )
    client.post(
        "/api/v1/motoristas",
        json={
            "nome": "Condutor B",
            "cnh": "22222222222",
            "validade_cnh": "2027-01-01",
            "cliente_id": cliente_b["id"],
        },
        headers=headers,
    )
    client.post(
        "/api/v1/motoristas",
        json={"nome": "Motorista sem vinculo", "cnh": "33333333333", "validade_cnh": "2027-01-01"},
        headers=headers,
    )

    resp_a = client.get(f"/api/v1/motoristas?cliente_id={cliente_a['id']}", headers=headers)
    assert resp_a.json()["meta"]["total"] == 1
    assert resp_a.json()["data"][0]["nome"] == "Condutor A"

    resp_todos = client.get("/api/v1/motoristas", headers=headers)
    assert resp_todos.json()["meta"]["total"] == 3


def test_motorista_sem_vinculo_continua_utilizavel_em_contrato(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_mot3@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "MOT1A23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()
    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Cliente Contrato", "documento": "44455566677"},
        headers=headers,
    ).json()
    motorista = client.post(
        "/api/v1/motoristas",
        json={"nome": "Motorista Geral", "cnh": "44444444444", "validade_cnh": "2027-01-01"},
        headers=headers,
    ).json()

    resp = client.post(
        "/api/v1/contratos",
        json={
            "cliente_id": cliente["id"],
            "veiculo_id": veiculo["id"],
            "motorista_id": motorista["id"],
            "data_inicio": "2026-10-01T10:00:00Z",
            "data_fim_prevista": "2026-10-05T10:00:00Z",
            "valor_diaria": "150.00",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["motorista_id"] == motorista["id"]
