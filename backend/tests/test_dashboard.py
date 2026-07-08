from tests.conftest import auth_headers, criar_usuario


def test_resumo_dashboard_administrador_ve_financeiro(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_dash@teste.com")
    headers = auth_headers(usuario)

    client.post(
        "/api/v1/veiculos",
        json={"placa": "DSH1A23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    )

    resp = client.get("/api/v1/dashboard/resumo", headers=headers)
    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["veiculos_por_status"]["disponivel"] == 1
    assert corpo["financeiro_mes"] is not None
    assert "receita" in corpo["financeiro_mes"]


def test_resumo_dashboard_mecanico_nao_ve_financeiro(client, db_session):
    usuario = criar_usuario(db_session, role="mecanico", email="mecanico_dash@teste.com")
    headers = auth_headers(usuario)

    resp = client.get("/api/v1/dashboard/resumo", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["financeiro_mes"] is None


def test_resumo_dashboard_alerta_licenciamento_vencendo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_dash2@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "ALR1D23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()
    client.patch(
        f"/api/v1/veiculos/{veiculo['id']}",
        json={"vencimento_seguro": "2020-01-01"},
        headers=headers,
    )

    resp = client.get("/api/v1/dashboard/resumo", headers=headers)
    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["veiculos_por_status"]["seguro_vencido"] == 1
    assert any(a["tipo"] == "seguro_vencido" for a in corpo["alertas"])
