from tests.conftest import auth_headers, criar_usuario


def test_criar_cliente_com_dossie_completo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_cli1@teste.com")
    headers = auth_headers(usuario)

    resp = client.post(
        "/api/v1/clientes",
        json={
            "nome": "Ana Paula",
            "documento": "11122233344",
            "rg": "1234567",
            "data_nascimento": "1985-03-20",
            "cnh_numero": "987654321",
            "cnh_categoria": "AB",
            "cnh_vencimento": "2027-01-01",
            "limite_credito": "3000.00",
            "banco": "Banco X",
            "pix": "ana@email.com",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    corpo = resp.json()
    assert corpo["cnh_categoria"] == "AB"
    assert corpo["status"] == "ativo"
    assert corpo["limite_credito"] == "3000.00"


def test_status_invalido_retorna_422(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_cli2@teste.com")
    headers = auth_headers(usuario)

    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Bruno", "documento": "22233344455"},
        headers=headers,
    ).json()

    resp = client.patch(
        f"/api/v1/clientes/{cliente['id']}",
        json={"status": "situacao_inexistente"},
        headers=headers,
    )
    assert resp.status_code == 422


def test_atualizar_status_para_bloqueado(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_cli3@teste.com")
    headers = auth_headers(usuario)

    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Carla", "documento": "33344455566"},
        headers=headers,
    ).json()

    resp = client.patch(
        f"/api/v1/clientes/{cliente['id']}",
        json={"status": "bloqueado"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "bloqueado"


def test_busca_cliente_por_nome_documento_telefone(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_cli4@teste.com")
    headers = auth_headers(usuario)

    client.post(
        "/api/v1/clientes",
        json={"nome": "Daniela Ferreira", "documento": "44455566677", "telefone": "11988887777"},
        headers=headers,
    )
    client.post(
        "/api/v1/clientes",
        json={"nome": "Eduardo Lima", "documento": "55566677788", "telefone": "11977776666"},
        headers=headers,
    )

    resp_nome = client.get("/api/v1/clientes?busca=Daniela", headers=headers)
    assert resp_nome.json()["meta"]["total"] == 1

    resp_documento = client.get("/api/v1/clientes?busca=555666777", headers=headers)
    assert resp_documento.json()["meta"]["total"] == 1

    resp_telefone = client.get("/api/v1/clientes?busca=977776666", headers=headers)
    assert resp_telefone.json()["meta"]["total"] == 1


def test_historico_cliente_alerta_cnh_vencendo_e_sem_pendencias(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_cli5@teste.com")
    headers = auth_headers(usuario)

    cliente = client.post(
        "/api/v1/clientes",
        json={
            "nome": "Fabio Nunes",
            "documento": "66677788899",
            "cnh_categoria": "B",
            "cnh_vencimento": "2020-01-01",
        },
        headers=headers,
    ).json()

    resp = client.get(f"/api/v1/clientes/{cliente['id']}/historico", headers=headers)
    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["ficha"]["locacoes_realizadas"] == 0
    assert corpo["ficha"]["avaliacao_estrelas"] == 3
    assert any(a["tipo"] == "cnh_vencida" for a in corpo["alertas"])


def test_historico_cliente_agrega_locacoes_e_financeiro(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_cli6@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "CLI1H23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()
    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Gustavo Reis", "documento": "77788899900"},
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
            "km_inicio": 500,
        },
        headers=headers,
    ).json()
    client.post(
        "/api/v1/financeiro/pagamentos",
        json={"contrato_id": contrato["id"], "valor": "600.00", "data": "2026-10-01T12:00:00Z"},
        headers=headers,
    )

    resp = client.get(f"/api/v1/clientes/{cliente['id']}/historico", headers=headers)
    assert resp.status_code == 200
    corpo = resp.json()
    assert corpo["ficha"]["locacao_atual"] is True
    assert corpo["ficha"]["veiculo_atual_placa"] == "CLI1H23"
    assert corpo["financeiro"]["total_pago"] == "600.00"
    assert len(corpo["locacoes"]) == 1
    assert corpo["locacoes"][0]["km_inicio"] == 500
