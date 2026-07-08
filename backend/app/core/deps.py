from collections.abc import Callable

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import has_permission
from app.core.security import decode_token
from app.exceptions import CredenciaisInvalidasError, PermissionDeniedError
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise CredenciaisInvalidasError("Token inválido para este tipo de operação.")
        user_id = payload.get("sub")
    except jwt.PyJWTError as exc:
        raise CredenciaisInvalidasError("Sessão expirada ou token inválido.") from exc

    user = db.get(Usuario, user_id)
    if user is None or not user.ativo:
        raise CredenciaisInvalidasError("Usuário inválido ou inativo.")
    return user


def require_permission(permission: str) -> Callable[[Usuario], Usuario]:
    def dependency(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if not has_permission(current_user.role, permission):
            raise PermissionDeniedError(
                f"Usuário não tem permissão '{permission}' para executar esta ação."
            )
        return current_user

    return dependency
