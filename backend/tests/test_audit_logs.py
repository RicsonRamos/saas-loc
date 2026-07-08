from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()


def test_atualizar_veiculo_gera_audit_log_com_diff(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_al1@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "AUD1A23")

    resp = client.patch(
        f"/api/v1/veiculos/{veiculo['id']}",
        json={"modelo": "Onix Plus"},
        headers=headers,
    )
    assert resp.status_code == 200

    logs_resp = client.get(
        "/api/v1/audit-logs",
        params={"entidade": "veiculo", "entidade_id": veiculo["id"]},
        headers=headers,
    )
    assert logs_resp.status_code == 200
    logs = logs_resp.json()["data"]

    log_atualizacao = next(log for log in logs if log["acao"] == "atualizar")
    assert log_atualizacao["entidade"] == "veiculo"
    assert log_atualizacao["entidade_id"] == veiculo["id"]
    assert log_atualizacao["dados_anteriores"]["modelo"] == "Onix"
    assert log_atualizacao["dados_novos"]["modelo"] == "Onix Plus"
    assert log_atualizacao["usuario_id"] == str(usuario.id)

    log_criacao = next(log for log in logs if log["acao"] == "criar")
    assert log_criacao["dados_novos"]["placa"] == "AUD1A23"


def test_auditoria_serializa_campos_decimal_e_date(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_al2@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "AUD2A23")

    resp = client.patch(
        f"/api/v1/veiculos/{veiculo['id']}",
        json={"valor_compra": "45000.50", "vencimento_seguro": "2027-01-15"},
        headers=headers,
    )
    assert resp.status_code == 200

    logs = client.get(
        "/api/v1/audit-logs",
        params={"entidade": "veiculo", "entidade_id": veiculo["id"]},
        headers=headers,
    ).json()["data"]
    log_atualizacao = next(log for log in logs if log["acao"] == "atualizar")
    assert log_atualizacao["dados_novos"]["valor_compra"] == "45000.50"
    assert log_atualizacao["dados_novos"]["vencimento_seguro"] == "2027-01-15"


def test_usuario_sem_permissao_recebe_403(client, db_session):
    usuario = criar_usuario(db_session, role="financeiro", email="fin_al1@teste.com")
    resp = client.get("/api/v1/audit-logs", headers=auth_headers(usuario))
    assert resp.status_code == 403
