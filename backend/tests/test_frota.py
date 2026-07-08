from tests.conftest import auth_headers, criar_usuario


def test_criar_veiculo_sem_permissao_retorna_403(client, db_session):
    usuario = criar_usuario(db_session, role="mecanico", email="mecanico@teste.com")

    response = client.post(
        "/api/v1/veiculos",
        json={"placa": "ABC1D23", "modelo": "Onix", "ano": 2023},
        headers=auth_headers(usuario),
    )

    assert response.status_code == 403


def test_criar_e_listar_veiculo_com_permissao(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin@teste.com")
    headers = auth_headers(usuario)

    criar_resp = client.post(
        "/api/v1/veiculos",
        json={"placa": "abc1d23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    )
    assert criar_resp.status_code == 201
    corpo = criar_resp.json()
    assert corpo["placa"] == "ABC1D23"
    assert corpo["status"] == "disponivel"

    listar_resp = client.get("/api/v1/veiculos", headers=headers)
    assert listar_resp.status_code == 200
    assert listar_resp.json()["meta"]["total"] == 1
