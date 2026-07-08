"""Exceções de domínio e handlers que as convertem em application/problem+json (RFC 9457).

Ver docs/04-API-CONVENCOES.md.
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

PROBLEM_BASE_URL = "https://app.locadora.com/problems"


class DomainError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "erro_dominio"
    title: str = "Erro de domínio"

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundError(DomainError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "recurso_nao_encontrado"
    title = "Recurso não encontrado"


class PermissionDeniedError(DomainError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "permissao_negada"
    title = "Permissão negada"


class ConflictError(DomainError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflito"
    title = "Conflito"


class VeiculoIndisponivelError(ConflictError):
    code = "veiculo_indisponivel"
    title = "Veículo indisponível"


class CredenciaisInvalidasError(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "credenciais_invalidas"
    title = "Credenciais inválidas"


def _problem_response(status_code: int, code: str, title: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        media_type="application/problem+json",
        content={
            "type": f"{PROBLEM_BASE_URL}/{code}",
            "title": title,
            "status": status_code,
            "detail": detail,
            "code": code.upper(),
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        return _problem_response(exc.status_code, exc.code, exc.title, exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            media_type="application/problem+json",
            content={
                "type": f"{PROBLEM_BASE_URL}/validation-error",
                "title": "Payload inválido",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "errors": [
                    {
                        "pointer": "/" + "/".join(str(p) for p in error["loc"][1:]),
                        "detail": error["msg"],
                    }
                    for error in exc.errors()
                ],
            },
        )
