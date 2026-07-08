from app.models.abastecimento import Abastecimento
from app.models.attachment import Attachment
from app.models.audit_log import AuditLog
from app.models.checklist import Assinatura, Checklist, ChecklistItem
from app.models.cliente import Cliente
from app.models.contrato import Contrato, ContratoEvento
from app.models.dano import Dano
from app.models.financeiro import Despesa, Pagamento
from app.models.manutencao import Manutencao
from app.models.motorista import Motorista
from app.models.multa import Multa
from app.models.pneu import Pneu
from app.models.sinistro import Sinistro
from app.models.usuario import Usuario
from app.models.vehicle_tracking import VehicleTracking
from app.models.veiculo import Veiculo

__all__ = [
    "Abastecimento",
    "Assinatura",
    "Attachment",
    "AuditLog",
    "Checklist",
    "ChecklistItem",
    "Cliente",
    "Contrato",
    "ContratoEvento",
    "Dano",
    "Despesa",
    "Pagamento",
    "Manutencao",
    "Motorista",
    "Multa",
    "Pneu",
    "Sinistro",
    "Usuario",
    "Veiculo",
    "VehicleTracking",
]
