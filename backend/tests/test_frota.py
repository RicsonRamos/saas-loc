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


def test_status_efetivo_licenciamento_vencido_quando_disponivel(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin6@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "VNC1D23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()

    client.patch(
        f"/api/v1/veiculos/{veiculo['id']}",
        json={"vencimento_licenciamento": "2020-01-01"},
        headers=headers,
    )

    obter_resp = client.get(f"/api/v1/veiculos/{veiculo['id']}", headers=headers)
    assert obter_resp.json()["status"] == "licenciamento_vencido"

    listar_resp = client.get("/api/v1/veiculos", headers=headers)
    veiculo_na_lista = next(v for v in listar_resp.json()["data"] if v["id"] == veiculo["id"])
    assert veiculo_na_lista["status"] == "licenciamento_vencido"


def test_status_efetivo_nao_sobrepoe_veiculo_em_manutencao(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin7@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "MNT1D23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()

    client.patch(
        f"/api/v1/veiculos/{veiculo['id']}",
        json={"vencimento_seguro": "2020-01-01", "status": "em_manutencao"},
        headers=headers,
    )

    obter_resp = client.get(f"/api/v1/veiculos/{veiculo['id']}", headers=headers)
    assert obter_resp.json()["status"] == "em_manutencao"


def test_atualizar_status_manual_para_sinistrado(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin8@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "SIN1D23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()

    resp = client.patch(
        f"/api/v1/veiculos/{veiculo['id']}",
        json={"status": "sinistrado"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "sinistrado"


def test_historico_veiculo_agrega_contratos_e_manutencoes(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin9@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "HST1D23", "modelo": "Onix", "ano": 2023},
        headers=headers,
    ).json()
    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Cliente Historico", "documento": "11122233344"},
        headers=headers,
    ).json()
    client.post(
        "/api/v1/contratos",
        json={
            "cliente_id": cliente["id"],
            "veiculo_id": veiculo["id"],
            "data_inicio": "2026-10-01T10:00:00Z",
            "data_fim_prevista": "2026-10-05T10:00:00Z",
            "valor_diaria": "199.90",
            "km_inicio": 1000,
        },
        headers=headers,
    )
    client.post(
        "/api/v1/manutencoes",
        json={
            "veiculo_id": veiculo["id"],
            "tipo": "preventiva",
            "data": "2026-09-01T09:00:00Z",
            "km": 900,
            "custo": "100.00",
        },
        headers=headers,
    )

    resp = client.get(f"/api/v1/veiculos/{veiculo['id']}/historico", headers=headers)
    assert resp.status_code == 200
    corpo = resp.json()
    assert len(corpo["contratos"]) == 1
    assert corpo["contratos"][0]["cliente_nome"] == "Cliente Historico"
    assert corpo["contratos"][0]["km_inicio"] == 1000
    assert len(corpo["manutencoes"]) == 1
    assert corpo["despesas"] == []
    assert any(e["origem"] == "manutencao" and e["km"] == 900 for e in corpo["eventos_km"])
    assert "indicadores" in corpo


def test_indicadores_veiculo_receita_custo_e_lucro(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin12@teste.com")
    headers = auth_headers(usuario)

    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "IND1A23", "modelo": "Onix", "ano": 2023, "km_atual": 1000},
        headers=headers,
    ).json()
    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Cliente Indicadores", "documento": "99988877700"},
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
        json={"data_fim_real": "2026-10-05T09:00:00Z", "km_final": 1400},
        headers=headers,
    )
    client.post(
        "/api/v1/financeiro/pagamentos",
        json={"contrato_id": contrato["id"], "valor": "600.00", "data": "2026-10-05T10:00:00Z"},
        headers=headers,
    )
    client.post(
        "/api/v1/manutencoes",
        json={
            "veiculo_id": veiculo["id"],
            "tipo": "preventiva",
            "data": "2026-10-06T09:00:00Z",
            "km": 1400,
            "custo": "100.00",
        },
        headers=headers,
    )
    client.post(
        "/api/v1/abastecimentos",
        json={
            "veiculo_id": veiculo["id"],
            "data": "2026-10-06T10:00:00Z",
            "litros": "20.000",
            "valor": "120.00",
            "km": 1400,
        },
        headers=headers,
    )

    resp = client.get(f"/api/v1/veiculos/{veiculo['id']}/historico", headers=headers)
    assert resp.status_code == 200
    indicadores = resp.json()["indicadores"]
    assert indicadores["receita_total"] == "600.00"
    assert indicadores["custo_total"] == "220.00"
    assert indicadores["lucro"] == "380.00"


def test_criar_veiculo_com_dossie_completo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin10@teste.com")
    headers = auth_headers(usuario)

    resp = client.post(
        "/api/v1/veiculos",
        json={
            "placa": "DOS1A23",
            "modelo": "Corolla",
            "ano": 2024,
            "marca": "Toyota",
            "versao": "XEI",
            "ano_fabricacao": 2023,
            "portas": 4,
            "capacidade_passageiros": 5,
            "motor": "2.0",
            "potencia": "177cv",
            "data_aquisicao": "2024-01-10",
            "valor_compra": "135000.00",
            "fornecedor": "Toyota Concessionaria",
            "km_inicial": 10,
            "proprietario": "Locadora XPTO",
            "crlv_numero": "123456",
            "ipva_vencimento": "2027-01-31",
            "alienado": True,
            "alienante": "Banco Y",
            "seguradora": "Porto Seguro",
            "apolice_numero": "AP-999",
            "seguro_franquia": "2500.00",
            "seguro_cobertura": "Compreensiva",
            "seguro_contato": "0800-123456",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    corpo = resp.json()
    assert corpo["ano_fabricacao"] == 2023
    assert corpo["valor_compra"] == "135000.00"
    assert corpo["alienado"] is True
    assert corpo["seguradora"] == "Porto Seguro"


def test_busca_e_filtros_na_listagem_de_veiculos(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin11@teste.com")
    headers = auth_headers(usuario)

    client.post(
        "/api/v1/veiculos",
        json={
            "placa": "FLT1A23",
            "modelo": "Corolla",
            "ano": 2024,
            "marca": "Toyota",
            "categoria": "Sedan",
        },
        headers=headers,
    )
    client.post(
        "/api/v1/veiculos",
        json={
            "placa": "FLT2A23",
            "modelo": "Onix",
            "ano": 2022,
            "marca": "Chevrolet",
            "categoria": "Hatch",
        },
        headers=headers,
    )

    resp_busca = client.get("/api/v1/veiculos?busca=Corolla", headers=headers)
    assert resp_busca.json()["meta"]["total"] == 1

    resp_marca = client.get("/api/v1/veiculos?marca=Chevrolet", headers=headers)
    assert resp_marca.json()["meta"]["total"] == 1
    assert resp_marca.json()["data"][0]["placa"] == "FLT2A23"

    resp_ano = client.get("/api/v1/veiculos?ano=2024", headers=headers)
    assert resp_ano.json()["meta"]["total"] == 1

    resp_categoria = client.get("/api/v1/veiculos?categoria=Hatch", headers=headers)
    assert resp_categoria.json()["meta"]["total"] == 1


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
