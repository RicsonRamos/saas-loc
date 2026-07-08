from tests.conftest import criar_usuario


def test_login_com_credenciais_invalidas_retorna_401(client):
    response = client.post(
        "/api/v1/auth/login", json={"email": "nao@existe.com", "password": "x"}
    )
    assert response.status_code == 401


def test_login_com_sucesso_retorna_token(client, db_session):
    criar_usuario(db_session, role="administrador", email="admin@teste.com")

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@teste.com", "password": "senha-forte-123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
