from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()


def test_ficha_pdf_autenticada_retorna_pdf(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_pdf1@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "PDF1A23")

    resp = client.get(f"/api/v1/veiculos/{veiculo['id']}/ficha.pdf", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content.startswith(b"%PDF")
    assert len(resp.content) > 0


def test_ficha_pdf_sem_token_retorna_401(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_pdf2@teste.com")
    veiculo = _criar_veiculo(client, auth_headers(usuario), "PDF2A23")

    resp = client.get(f"/api/v1/veiculos/{veiculo['id']}/ficha.pdf")
    assert resp.status_code == 401


def test_historico_abastecimentos_e_manutencoes_pdf(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_pdf3@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "PDF3A23")

    for caminho in ("historico.pdf", "abastecimentos.pdf", "manutencoes.pdf"):
        resp = client.get(f"/api/v1/veiculos/{veiculo['id']}/{caminho}", headers=headers)
        assert resp.status_code == 200, caminho
        assert resp.content.startswith(b"%PDF")
