from sqlalchemy.orm import Session
from models.schemas import ClienteSchema
from repositories.cliente_repository import ClienteRepository
from typing import List

class ClienteService:
    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    def listar_todos(self) -> List[ClienteSchema]:
        clientes = self.repo.get_all()
        return [ClienteSchema(**c.__dict__) for c in clientes]

    def criar(self, data: ClienteSchema) -> ClienteSchema:
        existente = self.repo.get_by_document(data.documento)
        if existente:
            raise ValueError(f"Cliente com documento {data.documento} já existe.")
        novo_cliente = self.repo.create(data.model_dump(exclude_unset=True))
        return ClienteSchema(**novo_cliente.__dict__)
