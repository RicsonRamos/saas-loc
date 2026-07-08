from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa):
    return client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()


def test_pneu_posicao_invalida_retorna_422(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_pn1@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "PNU1A23")

    resp = client.post(
        "/api/v1/pneus",
        json={
            "veiculo_id": veiculo["id"],
            "marca": "Pirelli",
            "posicao": "meio",
            "data_instalacao": "2026-01-01",
            "km_instalacao": 5000,
        },
        headers=headers,
    )
    assert resp.status_code == 422


def test_pneu_crud_completo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_pn2@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "PNU2A23")

    criar_resp = client.post(
        "/api/v1/pneus",
        json={
            "veiculo_id": veiculo["id"],
            "marca": "Pirelli",
            "modelo": "Cinturato",
            "posicao": "dianteiro_esquerdo",
            "data_instalacao": "2026-01-01",
            "km_instalacao": 5000,
            "vida_util_km": 40000,
        },
        headers=headers,
    )
    assert criar_resp.status_code == 201
    pneu = criar_resp.json()
    assert pneu["status"] == "ativo"

    trocar_resp = client.patch(
        f"/api/v1/pneus/{pneu['id']}",
        json={"status": "trocado", "data_troca": "2026-06-01", "km_troca": 45000},
        headers=headers,
    )
    assert trocar_resp.status_code == 200
    assert trocar_resp.json()["status"] == "trocado"

    listar_resp = client.get(f"/api/v1/pneus?veiculo_id={veiculo['id']}", headers=headers)
    assert listar_resp.json()["meta"]["total"] == 1

    remover_resp = client.delete(f"/api/v1/pneus/{pneu['id']}", headers=headers)
    assert remover_resp.status_code == 204


def test_mecanico_pode_registrar_pneu(client, db_session):
    admin = criar_usuario(db_session, role="administrador", email="admin_pn3@teste.com")
    veiculo = _criar_veiculo(client, auth_headers(admin), "PNU3A23")

    mecanico = criar_usuario(db_session, role="mecanico", email="mec_pn@teste.com")
    resp = client.post(
        "/api/v1/pneus",
        json={
            "veiculo_id": veiculo["id"],
            "marca": "Michelin",
            "posicao": "traseiro_direito",
            "data_instalacao": "2026-02-01",
            "km_instalacao": 1000,
        },
        headers=auth_headers(mecanico),
    )
    assert resp.status_code == 201
