from decimal import Decimal

from tests.conftest import auth_headers, criar_usuario


def _criar_contrato(client, headers):
    veiculo = client.post(
        "/api/v1/veiculos",
        json={"placa": "FIN1A23", "modelo": "Fiesta", "ano": 2021},
        headers=headers,
    ).json()
    cliente = client.post(
        "/api/v1/clientes",
        json={"nome": "Cliente Financeiro", "documento": "99988877766"},
        headers=headers,
    ).json()
    return client.post(
        "/api/v1/contratos",
        json={
            "cliente_id": cliente["id"],
            "veiculo_id": veiculo["id"],
            "data_inicio": "2026-10-01T10:00:00Z",
            "data_fim_prevista": "2026-10-05T10:00:00Z",
            "valor_diaria": "199.90",
        },
        headers=headers,
    ).json()


def test_pagamento_mantem_precisao_decimal_e_bloqueia_estorno_duplicado(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin@teste.com")
    headers = auth_headers(usuario)

    contrato = _criar_contrato(client, headers)

    pagamento_resp = client.post(
        "/api/v1/financeiro/pagamentos",
        json={"contrato_id": contrato["id"], "valor": "799.60", "data": "2026-10-05T12:00:00Z"},
        headers=headers,
    )
    assert pagamento_resp.status_code == 201
    pagamento = pagamento_resp.json()
    assert Decimal(pagamento["valor"]) == Decimal("799.60")

    estorno_resp = client.patch(
        f"/api/v1/financeiro/pagamentos/{pagamento['id']}/estorno", headers=headers
    )
    assert estorno_resp.status_code == 200
    assert estorno_resp.json()["status"] == "estornado"

    estorno_duplicado_resp = client.patch(
        f"/api/v1/financeiro/pagamentos/{pagamento['id']}/estorno", headers=headers
    )
    assert estorno_duplicado_resp.status_code == 409


def test_valor_de_pagamento_negativo_ou_zero_e_rejeitado(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin@teste.com")
    headers = auth_headers(usuario)

    contrato = _criar_contrato(client, headers)

    resp = client.post(
        "/api/v1/financeiro/pagamentos",
        json={"contrato_id": contrato["id"], "valor": "0.00", "data": "2026-10-05T12:00:00Z"},
        headers=headers,
    )
    assert resp.status_code == 422
