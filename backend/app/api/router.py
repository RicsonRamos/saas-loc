from fastapi import APIRouter

from app.api import auth, clientes, contratos, financeiro, frota, manutencoes, motoristas

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(frota.router)
api_router.include_router(clientes.router)
api_router.include_router(motoristas.router)
api_router.include_router(contratos.router)
api_router.include_router(manutencoes.router)
api_router.include_router(financeiro.router)
