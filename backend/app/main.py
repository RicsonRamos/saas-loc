import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.storage import garantir_buckets
from app.exceptions import register_exception_handlers

logger = logging.getLogger(__name__)

_storage_verificado = False


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Guard de processo: cada `TestClient(app)` (um por teste) dispara este
    # lifespan de novo. Sem isso, uma suíte inteira reexecuta a tentativa de
    # conexão ao MinIO (e paga o timeout de rede) uma vez por teste.
    global _storage_verificado
    if not _storage_verificado:
        _storage_verificado = True
        try:
            garantir_buckets()
        except Exception:
            # Storage (MinIO) é opcional para subir a API — falha aqui não deve
            # derrubar o backend inteiro, só os endpoints de anexo ficam indisponíveis.
            logger.warning(
                "Não foi possível conectar ao storage (MinIO) no startup.", exc_info=True
            )
    yield


app = FastAPI(title="Locadora SaaS API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
