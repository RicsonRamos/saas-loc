from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa):
    return client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()


def test_abastecimento_sem_permissao_retorna_403(client, db_session):
    admin = criar_usuario(db_session, role="administrador", email="admin_ab_setup@teste.com")
    veiculo = _criar_veiculo(client, auth_headers(admin), "ABS1A23")

    usuario = criar_usuario(db_session, role="financeiro", email="fin_ab@teste.com")
    resp = client.post(
        "/api/v1/abastecimentos",
        json={
            "veiculo_id": veiculo["id"],
            "data": "2026-07-01T10:00:00Z",
            "litros": "40.5",
            "valor": "250.00",
            "km": 5400,
        },
        headers=auth_headers(usuario),
    )
    assert resp.status_code == 403


def test_abastecimento_crud_e_valor_por_litro(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_ab@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "ABS2A23")

    criar_resp = client.post(
        "/api/v1/abastecimentos",
        json={
            "veiculo_id": veiculo["id"],
            "data": "2026-07-01T10:00:00Z",
            "posto": "Posto Ipiranga",
            "litros": "40.500",
            "valor": "250.00",
            "km": 5400,
            "tipo_combustivel": "Gasolina",
        },
        headers=headers,
    )
    assert criar_resp.status_code == 201
    abastecimento = criar_resp.json()
    assert abastecimento["valor_por_litro"] == "6.173"

    atualizar_resp = client.patch(
        f"/api/v1/abastecimentos/{abastecimento['id']}",
        json={"valor": "260.00"},
        headers=headers,
    )
    assert atualizar_resp.status_code == 200

    listar_resp = client.get(
        f"/api/v1/abastecimentos?veiculo_id={veiculo['id']}", headers=headers
    )
    assert listar_resp.json()["meta"]["total"] == 1

    remover_resp = client.delete(
        f"/api/v1/abastecimentos/{abastecimento['id']}", headers=headers
    )
    assert remover_resp.status_code == 204
