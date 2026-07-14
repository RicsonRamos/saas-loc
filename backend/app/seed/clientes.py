from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.cliente import (
    STATUS_ATIVO,
    STATUS_BLOQUEADO,
    STATUS_EM_ANALISE,
    STATUS_INADIMPLENTE,
    STATUS_INATIVO,
    Cliente,
)
from app.schemas.cliente import ClienteCreate
from app.seed.fake import escolher, fake, gerar_documento, unico

# Maioria ativo, mas com variedade suficiente para os cenários pedidos
# (cliente bloqueado, inadimplente etc. aparecerem nos filtros/telas).
_DISTRIBUICAO_STATUS = (
    [STATUS_ATIVO] * 70
    + [STATUS_BLOQUEADO] * 8
    + [STATUS_INADIMPLENTE] * 10
    + [STATUS_EM_ANALISE] * 7
    + [STATUS_INATIVO] * 5
)

_ESTADOS_BR = ["SP", "RJ", "MG", "PR", "RS", "SC", "BA", "PE", "CE", "GO", "DF"]


def _data_cnh_vencimento(hoje: date) -> date | None:
    """Distribui vencimentos entre vencida, vencendo em breve e confortavelmente válida."""
    r = fake.random.random()
    if r < 0.08:
        return hoje - timedelta(days=fake.random_int(1, 400))
    if r < 0.2:
        return hoje + timedelta(days=fake.random_int(1, 25))
    return hoje + timedelta(days=fake.random_int(60, 365 * 5))


def criar_clientes(db: Session, quantidade: int) -> list[Cliente]:
    """Insere os clientes em lote (bypassa `cliente_service.criar`, que só faz um
    insert simples sem efeito colateral em outra tabela — ver
    docs/10-SEED-DESENVOLVIMENTO.md para o racional de evitar milhares de round-trips
    individuais contra bancos remotos)."""
    hoje = date.today()
    usados_documento: set[str] = set()
    clientes: list[Cliente] = []

    for _ in range(quantidade):
        payload = ClienteCreate(
            nome=fake.name(),
            documento=unico(gerar_documento, usados_documento),
            rg=fake.numerify("##.###.###-#"),
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=75),
            email=fake.email(),
            telefone=fake.phone_number(),
            celular_secundario=fake.phone_number() if fake.random.random() < 0.3 else None,
            whatsapp=fake.phone_number() if fake.random.random() < 0.6 else None,
            cep=fake.postcode(),
            logradouro=fake.street_name(),
            numero=str(fake.random_int(1, 2000)),
            bairro=fake.bairro() if hasattr(fake, "bairro") else fake.city_suffix(),
            cidade=fake.city(),
            estado=escolher(_ESTADOS_BR),
            cnh_numero=fake.numerify("###########"),
            cnh_categoria=escolher(["A", "B", "AB", "D"]),
            cnh_vencimento=_data_cnh_vencimento(hoje),
            cnh_primeira_habilitacao=hoje - timedelta(days=fake.random_int(365, 365 * 20)),
            limite_credito=fake.random_int(1000, 20000),
            forma_pagamento_preferida=escolher(["pix", "cartao", "boleto", "dinheiro"]),
            caucao_padrao=fake.random_int(200, 2000),
        )
        cliente = Cliente(**payload.model_dump())
        cliente.status = escolher(_DISTRIBUICAO_STATUS)
        clientes.append(cliente)

    db.add_all(clientes)
    db.commit()
    print(f"  clientes: {len(clientes)} criados")
    return clientes
