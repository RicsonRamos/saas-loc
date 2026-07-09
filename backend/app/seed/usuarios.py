"""Usuários de desenvolvimento — não existe service dedicado (nenhum endpoint de
cadastro de usuário no sistema hoje), então insere direto via ORM, como já faz
`tests/conftest.py::criar_usuario`.
"""

from sqlalchemy.orm import Session

from app.core.permissions import ADMINISTRADOR, FINANCEIRO, MECANICO, OPERADOR
from app.core.security import hash_password
from app.models.usuario import Usuario
from app.seed.fake import fake

DOMINIO_SEED = "devseed.local"
SENHA_PADRAO = "DevSeed@123"

_DISTRIBUICAO_PAPEIS = (
    [ADMINISTRADOR] * 2
    + [OPERADOR] * 14
    + [FINANCEIRO] * 6
    + [MECANICO] * 8
)


def usuario_seed_ja_existe(db: Session) -> bool:
    from sqlalchemy import select

    return (
        db.scalar(select(Usuario).where(Usuario.email.like(f"%@{DOMINIO_SEED}"))) is not None
    )


def criar_usuarios(db: Session) -> list[Usuario]:
    senha_hash = hash_password(SENHA_PADRAO)
    usuarios: list[Usuario] = []
    usados_email: set[str] = set()

    for indice, papel in enumerate(_DISTRIBUICAO_PAPEIS):
        nome = fake.name()
        base_email = (
            nome.lower()
            .replace(" ", ".")
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        email = f"{base_email}.{indice}@{DOMINIO_SEED}"
        usados_email.add(email)
        usuarios.append(
            Usuario(
                nome=nome,
                email=email,
                password_hash=senha_hash,
                role=papel,
                ativo=True,
            )
        )

    db.add_all(usuarios)
    db.commit()
    for usuario in usuarios:
        db.refresh(usuario)
    print(f"  usuarios: {len(usuarios)} criados (senha: {SENHA_PADRAO!r})")
    return usuarios
