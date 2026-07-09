from fastapi import APIRouter

from app.api import (
    abastecimentos,
    attachments,
    audit_logs,
    auth,
    checklists,
    clientes,
    contratos,
    danos,
    dashboard,
    financeiro,
    frota,
    leituras_km,
    manutencoes,
    multas,
    planos_manutencao,
    pneus,
    sinistros,
    veiculo_publico,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(dashboard.router)
api_router.include_router(frota.router)
api_router.include_router(audit_logs.router)
api_router.include_router(attachments.router)
api_router.include_router(checklists.router)

# Sem Depends(require_permission) de propósito: única rota pública da API.
api_router.include_router(veiculo_publico.router)
api_router.include_router(clientes.router)
api_router.include_router(contratos.router)
api_router.include_router(manutencoes.router)
api_router.include_router(planos_manutencao.router)
api_router.include_router(financeiro.router)
api_router.include_router(multas.router)
api_router.include_router(sinistros.router)
api_router.include_router(danos.router)
api_router.include_router(abastecimentos.router)
api_router.include_router(pneus.router)
api_router.include_router(leituras_km.router)
