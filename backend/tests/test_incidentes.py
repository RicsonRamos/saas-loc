from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa):
    return client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()


def test_multa_sem_permissao_retorna_403(client, db_session):
    admin = criar_usuario(db_session, role="administrador", email="admin_multa_setup@teste.com")
    veiculo = _criar_veiculo(client, auth_headers(admin), "MUL1A23")

    usuario = criar_usuario(db_session, role="financeiro", email="fin_multa@teste.com")
    headers = auth_headers(usuario)

    resp = client.post(
        "/api/v1/multas",
        json={
            "veiculo_id": veiculo["id"],
            "data": "2026-07-01T10:00:00Z",
            "infracao": "Excesso de velocidade",
            "valor": "195.23",
        },
        headers=headers,
    )
    assert resp.status_code == 403


def test_multa_crud_completo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_multa@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "MUL2A23")

    criar_resp = client.post(
        "/api/v1/multas",
        json={
            "veiculo_id": veiculo["id"],
            "data": "2026-07-01T10:00:00Z",
            "infracao": "Excesso de velocidade",
            "local": "Av. Paulista",
            "valor": "195.23",
            "pontos": 5,
        },
        headers=headers,
    )
    assert criar_resp.status_code == 201
    multa = criar_resp.json()
    assert multa["status"] == "pendente"

    atualizar_resp = client.patch(
        f"/api/v1/multas/{multa['id']}",
        json={"status": "paga"},
        headers=headers,
    )
    assert atualizar_resp.status_code == 200
    assert atualizar_resp.json()["status"] == "paga"

    listar_resp = client.get(
        f"/api/v1/multas?veiculo_id={veiculo['id']}", headers=headers
    )
    assert listar_resp.json()["meta"]["total"] == 1

    remover_resp = client.delete(f"/api/v1/multas/{multa['id']}", headers=headers)
    assert remover_resp.status_code == 204

    obter_resp = client.get(f"/api/v1/multas/{multa['id']}", headers=headers)
    assert obter_resp.status_code == 404


def test_multa_status_invalido_retorna_422(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_multa2@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "MUL3A23")

    resp = client.post(
        "/api/v1/multas",
        json={
            "veiculo_id": veiculo["id"],
            "data": "2026-07-01T10:00:00Z",
            "infracao": "Excesso de velocidade",
            "valor": "100.00",
            "status": "situacao_inexistente",
        },
        headers=headers,
    )
    assert resp.status_code == 422


def test_sinistro_crud_e_tipo_invalido(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_sin@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "SIN2A23")

    criar_resp = client.post(
        "/api/v1/sinistros",
        json={
            "veiculo_id": veiculo["id"],
            "tipo": "batida",
            "data": "2026-07-02T10:00:00Z",
            "descricao": "Colisão traseira leve",
        },
        headers=headers,
    )
    assert criar_resp.status_code == 201
    sinistro = criar_resp.json()
    assert sinistro["status"] == "aberto"

    invalido_resp = client.post(
        "/api/v1/sinistros",
        json={
            "veiculo_id": veiculo["id"],
            "tipo": "tornado",
            "data": "2026-07-02T10:00:00Z",
        },
        headers=headers,
    )
    assert invalido_resp.status_code == 422

    atualizar_resp = client.patch(
        f"/api/v1/sinistros/{sinistro['id']}",
        json={"status": "finalizado", "seguradora_acionada": True},
        headers=headers,
    )
    assert atualizar_resp.status_code == 200
    assert atualizar_resp.json()["seguradora_acionada"] is True

    remover_resp = client.delete(f"/api/v1/sinistros/{sinistro['id']}", headers=headers)
    assert remover_resp.status_code == 204


def test_dano_crud_e_mecanico_pode_registrar(client, db_session):
    usuario = criar_usuario(db_session, role="mecanico", email="mec_dano@teste.com")
    headers = auth_headers(usuario)

    admin = criar_usuario(db_session, role="administrador", email="admin_dano@teste.com")
    veiculo = _criar_veiculo(client, headers=auth_headers(admin), placa="DAN2A23")

    criar_resp = client.post(
        "/api/v1/danos",
        json={
            "veiculo_id": veiculo["id"],
            "tipo": "arranhao",
            "data": "2026-07-03",
            "descricao": "Arranhão na porta direita",
        },
        headers=headers,
    )
    assert criar_resp.status_code == 201
    dano = criar_resp.json()

    atualizar_resp = client.patch(
        f"/api/v1/danos/{dano['id']}",
        json={"status": "reparado", "valor_reparo": "80.00"},
        headers=headers,
    )
    assert atualizar_resp.status_code == 200
    assert atualizar_resp.json()["status"] == "reparado"


def test_historico_veiculo_inclui_multas_sinistros_danos(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_hist_inc@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "HST2A23")

    client.post(
        "/api/v1/multas",
        json={
            "veiculo_id": veiculo["id"],
            "data": "2026-07-01T10:00:00Z",
            "infracao": "Excesso de velocidade",
            "valor": "100.00",
        },
        headers=headers,
    )
    client.post(
        "/api/v1/sinistros",
        json={"veiculo_id": veiculo["id"], "tipo": "furto", "data": "2026-07-02T10:00:00Z"},
        headers=headers,
    )
    client.post(
        "/api/v1/danos",
        json={"veiculo_id": veiculo["id"], "tipo": "amassado", "data": "2026-07-03"},
        headers=headers,
    )

    resp = client.get(f"/api/v1/veiculos/{veiculo['id']}/historico", headers=headers)
    assert resp.status_code == 200
    corpo = resp.json()
    assert len(corpo["multas"]) == 1
    assert len(corpo["sinistros"]) == 1
    assert len(corpo["danos"]) == 1


def test_dashboard_alerta_multa_pendente(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_dash_multa@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "DSH2A23")

    client.post(
        "/api/v1/multas",
        json={
            "veiculo_id": veiculo["id"],
            "data": "2026-07-01T10:00:00Z",
            "infracao": "Excesso de velocidade",
            "valor": "100.00",
        },
        headers=headers,
    )

    resp = client.get("/api/v1/dashboard/resumo", headers=headers)
    assert resp.status_code == 200
    alertas = resp.json()["alertas"]
    assert any(a["tipo"] == "multas_pendentes" and a["veiculo_placa"] == "DSH2A23" for a in alertas)


def test_historico_cliente_inclui_multas_e_reduz_avaliacao(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_hist_cli_inc@teste.com")
    headers = auth_headers(usuario)

    veiculo = _criar_veiculo(client, headers, "CLM1A23")
    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Helena Costa", "documento": "88899900011"},
        headers=headers,
    ).json()
    contrato = client.post(
        "/api/v1/contratos",
        json={
            "cliente_id": cliente["id"],
            "veiculo_id": veiculo["id"],
            "data_inicio": "2026-10-01T10:00:00Z",
            "data_fim_prevista": "2026-10-05T10:00:00Z",
            "valor_diaria": "150.00",
        },
        headers=headers,
    ).json()
    client.patch(
        f"/api/v1/contratos/{contrato['id']}/devolucao",
        json={"data_fim_real": "2026-10-05T09:00:00Z"},
        headers=headers,
    )

    client.post(
        "/api/v1/multas",
        json={
            "veiculo_id": veiculo["id"],
            "cliente_id": cliente["id"],
            "data": "2026-10-02T10:00:00Z",
            "infracao": "Estacionamento irregular",
            "valor": "50.00",
        },
        headers=headers,
    )

    resp = client.get(f"/api/v1/clientes/{cliente['id']}/historico", headers=headers)
    assert resp.status_code == 200
    corpo = resp.json()
    assert len(corpo["multas"]) == 1
    assert any(a["tipo"] == "multas_pendentes" for a in corpo["alertas"])
    assert corpo["ficha"]["avaliacao_estrelas"] == 4
