import pytest

from app.core.storage import garantir_buckets
from tests.conftest import auth_headers, criar_usuario


def _storage_disponivel() -> bool:
    try:
        garantir_buckets()
        return True
    except Exception:
        return False


def _criar_veiculo(client, headers, placa):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "HB20", "ano": 2022},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def _criar_cliente(client, headers, documento):
    resp = client.post(
        "/api/v1/clientes", json={"nome": "Cliente Teste", "documento": documento}, headers=headers
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def _criar_contrato(client, headers, veiculo_id, cliente_id):
    resp = client.post(
        "/api/v1/contratos",
        json={
            "cliente_id": cliente_id,
            "veiculo_id": veiculo_id,
            "data_inicio": "2026-08-01T10:00:00Z",
            "data_fim_prevista": "2026-08-05T10:00:00Z",
            "valor_diaria": "150.00",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()


def _payload_checklist(contrato_id, tipo):
    return {
        "contrato_id": contrato_id,
        "tipo": tipo,
        "data": "2026-08-01T09:00:00Z",
        "km": 1000 if tipo == "entrega" else 1200,
        "combustivel": "cheio",
        "itens": [
            {"item": "lataria", "situacao": "ok"},
            {"item": "pneus", "situacao": "ok" if tipo == "entrega" else "avaria"},
            {"item": "combustivel", "situacao": "ok"},
            {"item": "km", "situacao": "ok"},
            {"item": "documentos", "situacao": "ok"},
            {"item": "acessorios", "situacao": "ok"},
        ],
    }


def test_checklist_entrega_exige_contrato_ativo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_chk1@teste.com")
    headers = auth_headers(usuario)
    veiculo_id = _criar_veiculo(client, headers, "CHK1A23")
    cliente_id = _criar_cliente(client, headers, "10000000001")
    contrato = _criar_contrato(client, headers, veiculo_id, cliente_id)

    client.patch(f"/api/v1/contratos/{contrato['id']}/cancelamento", headers=headers)

    resp = client.post(
        "/api/v1/checklists", json=_payload_checklist(contrato["id"], "entrega"), headers=headers
    )
    assert resp.status_code == 409


def test_checklist_devolucao_exige_entrega_previa(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_chk2@teste.com")
    headers = auth_headers(usuario)
    veiculo_id = _criar_veiculo(client, headers, "CHK2A23")
    cliente_id = _criar_cliente(client, headers, "10000000002")
    contrato = _criar_contrato(client, headers, veiculo_id, cliente_id)

    resp = client.post(
        "/api/v1/checklists",
        json=_payload_checklist(contrato["id"], "devolucao"),
        headers=headers,
    )
    assert resp.status_code == 409


def test_checklist_duplicado_mesmo_tipo_retorna_409(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_chk3@teste.com")
    headers = auth_headers(usuario)
    veiculo_id = _criar_veiculo(client, headers, "CHK3A23")
    cliente_id = _criar_cliente(client, headers, "10000000003")
    contrato = _criar_contrato(client, headers, veiculo_id, cliente_id)

    payload = _payload_checklist(contrato["id"], "entrega")
    assert client.post("/api/v1/checklists", json=payload, headers=headers).status_code == 201
    resp = client.post("/api/v1/checklists", json=payload, headers=headers)
    assert resp.status_code == 409


def test_comparacao_entrega_devolucao_mostra_diferencas(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_chk4@teste.com")
    headers = auth_headers(usuario)
    veiculo_id = _criar_veiculo(client, headers, "CHK4A23")
    cliente_id = _criar_cliente(client, headers, "10000000004")
    contrato = _criar_contrato(client, headers, veiculo_id, cliente_id)

    entrega_resp = client.post(
        "/api/v1/checklists",
        json=_payload_checklist(contrato["id"], "entrega"),
        headers=headers,
    )
    assert entrega_resp.status_code == 201

    devolucao_resp = client.post(
        "/api/v1/checklists",
        json=_payload_checklist(contrato["id"], "devolucao"),
        headers=headers,
    )
    assert devolucao_resp.status_code == 201

    comparacao_resp = client.get(
        f"/api/v1/contratos/{contrato['id']}/checklists/comparacao", headers=headers
    )
    assert comparacao_resp.status_code == 200
    itens = {item["item"]: item for item in comparacao_resp.json()["itens"]}

    assert itens["pneus"]["situacao_entrega"] == "ok"
    assert itens["pneus"]["situacao_devolucao"] == "avaria"
    assert itens["pneus"]["mudou"] is True

    assert itens["lataria"]["mudou"] is False


def test_comparacao_sem_devolucao_retorna_409(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_chk5@teste.com")
    headers = auth_headers(usuario)
    veiculo_id = _criar_veiculo(client, headers, "CHK5A23")
    cliente_id = _criar_cliente(client, headers, "10000000005")
    contrato = _criar_contrato(client, headers, veiculo_id, cliente_id)

    client.post(
        "/api/v1/checklists", json=_payload_checklist(contrato["id"], "entrega"), headers=headers
    )

    resp = client.get(f"/api/v1/contratos/{contrato['id']}/checklists/comparacao", headers=headers)
    assert resp.status_code == 409


@pytest.mark.skipif(
    not _storage_disponivel(),
    reason="Storage indisponível (configure STORAGE_* no .env para rodar este teste)",
)
def test_assinatura_vincula_attachment_ao_checklist(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_chk6@teste.com")
    headers = auth_headers(usuario)
    veiculo_id = _criar_veiculo(client, headers, "CHK6A23")
    cliente_id = _criar_cliente(client, headers, "10000000006")
    contrato = _criar_contrato(client, headers, veiculo_id, cliente_id)

    checklist = client.post(
        "/api/v1/checklists", json=_payload_checklist(contrato["id"], "entrega"), headers=headers
    ).json()

    png = bytes.fromhex(
        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
        "890000000a49444154789c6360000002000100ffff03000006000557bf"
        "abd4000000004945454e44ae426082"
    )
    attachment = client.post(
        "/api/v1/attachments",
        data={"entidade_tipo": "assinatura", "entidade_id": checklist["id"]},
        files={"arquivo": ("assinatura.png", png, "image/png")},
        headers=headers,
    ).json()

    resp = client.post(
        f"/api/v1/checklists/{checklist['id']}/assinaturas",
        json={"attachment_id": attachment["id"], "responsavel_nome": "João da Silva"},
        headers=headers,
    )
    assert resp.status_code == 201
    corpo = resp.json()
    assert corpo["checklist_id"] == checklist["id"]
    assert corpo["attachment_id"] == attachment["id"]
    assert corpo["responsavel_nome"] == "João da Silva"


@pytest.mark.skipif(
    not _storage_disponivel(),
    reason="Storage indisponível (configure STORAGE_* no .env para rodar este teste)",
)
def test_vincula_foto_a_item_do_checklist(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_chk7@teste.com")
    headers = auth_headers(usuario)
    veiculo_id = _criar_veiculo(client, headers, "CHK7A23")
    cliente_id = _criar_cliente(client, headers, "10000000007")
    contrato = _criar_contrato(client, headers, veiculo_id, cliente_id)

    checklist = client.post(
        "/api/v1/checklists", json=_payload_checklist(contrato["id"], "entrega"), headers=headers
    ).json()
    item = checklist["itens"][0]

    png = bytes.fromhex(
        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
        "890000000a49444154789c6360000002000100ffff03000006000557bf"
        "abd4000000004945454e44ae426082"
    )
    attachment = client.post(
        "/api/v1/attachments",
        data={"entidade_tipo": "checklist_item", "entidade_id": item["id"]},
        files={"arquivo": ("dano.png", png, "image/png")},
        headers=headers,
    ).json()

    resp = client.patch(
        f"/api/v1/checklists/{checklist['id']}/itens/{item['id']}",
        json={"foto_attachment_id": attachment["id"]},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["foto_attachment_id"] == attachment["id"]

    checklist_atualizado = client.get(
        f"/api/v1/checklists/{checklist['id']}", headers=headers
    ).json()
    item_atualizado = next(i for i in checklist_atualizado["itens"] if i["id"] == item["id"])
    assert item_atualizado["foto_attachment_id"] == attachment["id"]


def test_foto_de_item_de_outro_checklist_retorna_404(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_chk8@teste.com")
    headers = auth_headers(usuario)
    veiculo_id = _criar_veiculo(client, headers, "CHK8A23")
    cliente_id = _criar_cliente(client, headers, "10000000008")
    contrato = _criar_contrato(client, headers, veiculo_id, cliente_id)

    checklist = client.post(
        "/api/v1/checklists", json=_payload_checklist(contrato["id"], "entrega"), headers=headers
    ).json()
    item = checklist["itens"][0]

    import uuid

    resp = client.patch(
        f"/api/v1/checklists/{uuid.uuid4()}/itens/{item['id']}",
        json={"foto_attachment_id": str(uuid.uuid4())},
        headers=headers,
    )
    assert resp.status_code == 404
