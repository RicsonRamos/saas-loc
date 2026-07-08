from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, verify_password
from app.exceptions import CredenciaisInvalidasError
from app.models.usuario import Usuario


def autenticar(db: Session, email: str, password: str) -> tuple[str, str]:
    stmt = select(Usuario).where(Usuario.email == email, Usuario.deleted_at.is_(None))
    usuario = db.execute(stmt).scalar_one_or_none()

    if usuario is None or not usuario.ativo or not verify_password(password, usuario.password_hash):
        raise CredenciaisInvalidasError("E-mail ou senha inválidos.")

    access_token = create_access_token(str(usuario.id), {"role": usuario.role})
    refresh_token = create_refresh_token(str(usuario.id))
    return access_token, refresh_token
