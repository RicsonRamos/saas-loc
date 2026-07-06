from sqlalchemy.orm import Session
from models.schemas import VeiculoSchema
from repositories.veiculo_repository import VeiculoRepository
from typing import List

class VeiculoService:
    def __init__(self, db: Session):
        self.repo = VeiculoRepository(db)

    def listar_todos(self) -> List[VeiculoSchema]:
        veiculos = self.repo.get_all()
        return [VeiculoSchema(**v.__dict__) for v in veiculos]

    def listar_disponiveis(self) -> List[VeiculoSchema]:
        veiculos = self.repo.get_disponiveis()
        return [VeiculoSchema(**v.__dict__) for v in veiculos]

    def criar(self, data: VeiculoSchema) -> VeiculoSchema:
        existente = self.repo.get_by_placa(data.placa)
        if existente:
            raise ValueError(f"Veículo com placa {data.placa} já existe.")
        novo_veiculo = self.repo.create(data.model_dump(exclude_unset=True))
        return VeiculoSchema(**novo_veiculo.__dict__)

    def atualizar_status(self, veiculo_id: str, status: str):
        veiculo = self.repo.get_by_id(veiculo_id)
        if veiculo:
            self.repo.update(veiculo, {"status": status})
