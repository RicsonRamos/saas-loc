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


def test_atualizar_veiculo_com_campos_adicionais(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin2@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "UPD1A23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()

    resp = client.patch(
        f"/api/v1/veiculos/{veiculo['id']}",
        json={
            "marca": "Chevrolet",
            "cor": "Prata",
            "categoria": "Hatch",
            "chassi": "9BWZZZ377VT004251",
            "renavam": "12345678901",
            "combustivel": "Flex",
            "cambio": "Automático",
            "vencimento_licenciamento": "2027-01-15",
            "vencimento_seguro": "2027-03-20",
        },
        headers=headers,
    )
    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["marca"] == "Chevrolet"
    assert corpo["chassi"] == "9BWZZZ377VT004251"
    assert corpo["vencimento_seguro"] == "2027-03-20"


def test_remover_veiculo_soft_delete_some_da_listagem(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin3@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "DEL1A23", "modelo": "Gol", "ano": 2020},
        headers=headers,
    ).json()

    del_resp = client.delete(f"/api/v1/veiculos/{veiculo['id']}", headers=headers)
    assert del_resp.status_code == 204

    obter_resp = client.get(f"/api/v1/veiculos/{veiculo['id']}", headers=headers)
    assert obter_resp.status_code == 404
