import pytest
from botocore.exceptions import EndpointConnectionError

from app.core.storage import garantir_buckets
from tests.conftest import auth_headers, criar_usuario


def _minio_disponivel() -> bool:
    try:
        garantir_buckets()
        return True
    except EndpointConnectionError:
        return False
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _minio_disponivel(),
    reason="MinIO indisponível (suba `docker compose up minio` para rodar estes testes)",
)


def _criar_veiculo(client, headers, placa):
    resp = client.post(
        "/api/v1/veiculos",
        json={"placa": placa, "modelo": "Onix", "ano": 2023},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()


def _png_minusculo() -> bytes:
    # PNG 1x1 válido (magic bytes reais), suficiente para o detector de content-type.
    return bytes.fromhex(
        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
        "890000000a49444154789c6360000002000100ffff03000006000557bf"
        "abd4000000004945454e44ae426082"
    )


def test_upload_download_e_exclusao_de_anexo(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_att1@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "ATT1A23")

    upload_resp = client.post(
        "/api/v1/attachments",
        data={"entidade_tipo": "veiculo", "entidade_id": veiculo["id"]},
        files={"arquivo": ("foto.png", _png_minusculo(), "image/png")},
        headers=headers,
    )
    assert upload_resp.status_code == 201
    attachment = upload_resp.json()
    assert attachment["content_type"] == "image/png"
    assert attachment["tipo"] == "imagem"

    listar_resp = client.get(
        "/api/v1/attachments",
        params={"entidade_tipo": "veiculo", "entidade_id": veiculo["id"]},
        headers=headers,
    )
    assert listar_resp.json()["meta"]["total"] == 1

    download_resp = client.get(
        f"/api/v1/attachments/{attachment['id']}/download", headers=headers
    )
    assert download_resp.status_code == 200
    assert download_resp.json()["url"].startswith("http")

    remover_resp = client.delete(f"/api/v1/attachments/{attachment['id']}", headers=headers)
    assert remover_resp.status_code == 204

    listar_apos_resp = client.get(
        "/api/v1/attachments",
        params={"entidade_tipo": "veiculo", "entidade_id": veiculo["id"]},
        headers=headers,
    )
    assert listar_apos_resp.json()["meta"]["total"] == 0


def test_upload_tipo_nao_suportado_retorna_422(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_att2@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "ATT2A23")

    resp = client.post(
        "/api/v1/attachments",
        data={"entidade_tipo": "veiculo", "entidade_id": veiculo["id"]},
        files={"arquivo": ("virus.exe", b"MZ-fake-executable-content", "application/octet-stream")},
        headers=headers,
    )
    assert resp.status_code == 422


def test_upload_entidade_tipo_invalido_retorna_422(client, db_session):
    usuario = criar_usuario(db_session, role="administrador", email="admin_att3@teste.com")
    headers = auth_headers(usuario)
    veiculo = _criar_veiculo(client, headers, "ATT3A23")

    resp = client.post(
        "/api/v1/attachments",
        data={"entidade_tipo": "algo-invalido", "entidade_id": veiculo["id"]},
        files={"arquivo": ("foto.png", _png_minusculo(), "image/png")},
        headers=headers,
    )
    assert resp.status_code == 422
