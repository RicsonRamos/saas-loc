"""Cria o primeiro usuário administrador. Uso: python create_admin.py <email> <senha> <nome>"""

import sys

from app.core.database import SessionLocal
from app.core.permissions import ADMINISTRADOR
from app.core.security import hash_password
from app.models.usuario import Usuario


def main() -> None:
    if len(sys.argv) != 4:
        print("Uso: python create_admin.py <email> <senha> <nome>")
        raise SystemExit(1)

    email, senha, nome = sys.argv[1], sys.argv[2], sys.argv[3]

    db = SessionLocal()
    try:
        if db.query(Usuario).filter(Usuario.email == email).first():
            print(f"Usuário {email} já existe.")
            return

        usuario = Usuario(
            nome=nome,
            email=email,
            password_hash=hash_password(senha),
            role=ADMINISTRADOR,
            ativo=True,
        )
        db.add(usuario)
        db.commit()
        print(f"Administrador {email} criado com sucesso.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
