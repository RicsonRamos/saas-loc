from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023, "chassi": "CHASSI-SIGILOSO-123"},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()


def test_consulta_publica_sem_token_retorna_dados_nao_sensiveis(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_pub1@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "PUB1A23")

    resp = client.get(f"/api/v1/veiculo/public/{veiculo['codigo_publico']}")
    assert resp.status_code == 200
    corpo = resp.json()

    assert corpo["placa"] == "PUB1A23"
    assert corpo["modelo"] == "Onix"
    assert corpo["status"] == "disponivel"
    assert corpo["locacao_atual"] == {"em_uso": False, "data_fim_prevista": None}
    assert "chassi" not in corpo
    assert "id" not in corpo
    assert "renavam" not in corpo


def test_consulta_publica_codigo_invalido_retorna_404(client, db_session):
    resp = client.get("/api/v1/veiculo/public/codigo-que-nao-existe")
    assert resp.status_code == 404


def test_regenerar_codigo_publico_invalida_o_anterior(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_pub2@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "PUB2A23")
    codigo_antigo = veiculo["codigo_publico"]

    regenerar_resp = client.post(
        f"/api/v1/veiculos/{veiculo['id']}/regenerar-codigo-publico", headers=headers
    )
    assert regenerar_resp.status_code == 200
    novo_codigo = regenerar_resp.json()["codigo_publico"]
    assert novo_codigo != codigo_antigo

    assert client.get(f"/api/v1/veiculo/public/{codigo_antigo}").status_code == 404
    assert client.get(f"/api/v1/veiculo/public/{novo_codigo}").status_code == 200
