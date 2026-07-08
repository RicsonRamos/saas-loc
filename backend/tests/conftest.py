import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.database import Base, get_db
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models import *  # noqa: F401,F403  garante que todas as tabelas sejam registradas
from app.models.contrato import SQL_CONSTRAINT_SEM_OVERLAP, SQL_HABILITAR_BTREE_GIST
from app.models.usuario import Usuario

TEST_DATABASE_URL = settings.database_url.rsplit("/", 1)[0] + "/locadora_test"


@pytest.fixture(scope="session")
def engine():
    eng = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(eng)
    Base.metadata.create_all(eng)
    with eng.begin() as conn:
        conn.exec_driver_sql(SQL_HABILITAR_BTREE_GIST)
        conn.exec_driver_sql(SQL_CONSTRAINT_SEM_OVERLAP)
    yield eng
    eng.dispose()


@pytest.fixture()
def db_session(engine) -> Session:
    """Sessão isolada por teste: tudo roda em uma transação que é desfeita ao final."""
    connection = engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    session = session_factory()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session: Session) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def criar_usuario(db_session: Session, role: str, email: str = "user@teste.com") -> Usuario:
    usuario = Usuario(
        nome="Usuário Teste",
        email=email,
        password_hash=hash_password("senha-forte-123"),
        role=role,
        ativo=True,
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario


def token_para(usuario: Usuario) -> str:
    return create_access_token(str(usuario.id), {"role": usuario.role})


def auth_headers(usuario: Usuario) -> dict[str, str]:
    return {"Authorization": f"Bearer {token_para(usuario)}"}
