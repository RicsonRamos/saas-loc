from datetime import UTC, datetime, timedelta

from tests.conftest import auth_headers, criar_usuario


def _criar_veiculo(client, headers, placa="PLN1M23", km_atual=10000):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023, "km_atual": km_atual},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def test_plano_normal_quando_muito_km_restante(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="plano1@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="PLN1A23", km_atual=1000)

    resp = client.post(
        "/api/v1/planos-manutencao",
        json={
            "veiculo_id": veiculo_id,
            "tipo": "troca_oleo",
            "intervalo_km": 5000,
            "ultima_execucao_km": 1000,
        },
        headers=headers,
    )
    assert resp.status_code == 201
    corpo = resp.json()
    assert corpo["prioridade"] == "normal"
    assert corpo["faltam_km"] == 5000


def test_plano_critico_quando_vencido_gera_alerta_dashboard(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="plano2@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="PLN2A23", km_atual=6500)

    resp = client.post(
        "/api/v1/planos-manutencao",
        json={
            "veiculo_id": veiculo_id,
            "tipo": "pastilhas_freio",
            "intervalo_km": 5000,
            "ultima_execucao_km": 1000,
        },
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["prioridade"] == "critico"

    dashboard_resp = client.get("/api/v1/dashboard/resumo", headers=headers)
    assert dashboard_resp.status_code == 200
    alertas = dashboard_resp.json()["alertas"]
    assert any(
        a["tipo"] == "manutencao_pastilhas_freio" and a["prioridade"] == "critico"
        for a in alertas
    )


def test_plano_por_data_atencao_proximo_do_vencimento(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="plano3@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="PLN3A23")
    hoje = datetime.now(UTC).date()

    resp = client.post(
        "/api/v1/planos-manutencao",
        json={
            "veiculo_id": veiculo_id,
            "tipo": "licenciamento",
            "intervalo_dias": 365,
            "ultima_execucao_data": (hoje - timedelta(days=300)).isoformat(),
        },
        headers=headers,
    )
    assert resp.status_code == 201
    assert resp.json()["prioridade"] == "atencao"


def test_plano_sem_intervalo_retorna_422(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="plano4@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="PLN4A23")

    resp = client.post(
        "/api/v1/planos-manutencao",
        json={"veiculo_id": veiculo_id, "tipo": "outro", "descricao": "Item customizado"},
        headers=headers,
    )
    assert resp.status_code == 422


def test_atualizar_e_remover_plano_manutencao(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="plano5@teste.com")
    headers = auth_headers(usuario)

    veiculo_id = _criar_veiculo(client, headers, placa="PLN5A23")

    plano = client.post(
        "/api/v1/planos-manutencao",
        json={"veiculo_id": veiculo_id, "tipo": "pneus", "intervalo_km": 40000},
        headers=headers,
    ).json()

    atualizar_resp = client.patch(
        f"/api/v1/planos-manutencao/{plano['id']}",
        json={"ultima_execucao_km": 5000},
        headers=headers,
    )
    assert atualizar_resp.status_code == 200
    assert atualizar_resp.json()["ultima_execucao_km"] == 5000

    remover_resp = client.delete(f"/api/v1/planos-manutencao/{plano['id']}", headers=headers)
    assert remover_resp.status_code == 204

    listagem = client.get(
        "/api/v1/planos-manutencao", params={"veiculo_id": veiculo_id}, headers=headers
    ).json()
    assert listagem["meta"]["total"] == 0
