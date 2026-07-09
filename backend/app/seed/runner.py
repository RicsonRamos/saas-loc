import time

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.seed.clientes import criar_clientes
from app.seed.contratos import criar_contratos
from app.seed.financeiro import (
    criar_danos,
    criar_despesas,
    criar_multas,
    criar_pagamentos,
    criar_sinistros,
)
from app.seed.manutencao import criar_manutencoes, criar_planos_manutencao
from app.seed.pneus_abastecimentos import criar_abastecimentos, criar_pneus
from app.seed.quilometragem import criar_leituras_km, criar_vehicle_tracking
from app.seed.usuarios import DOMINIO_SEED, usuario_seed_ja_existe
from app.seed.usuarios import criar_usuarios as _criar_usuarios
from app.seed.veiculos import criar_veiculos

# Ordem de TRUNCATE: CASCADE cuida das dependências de FK automaticamente, então a
# ordem desta lista não precisa respeitar a árvore de dependências — só precisa
# cobrir todas as tabelas da aplicação.
_TABELAS_APP = [
    "assinaturas",
    "checklist_itens",
    "checklists",
    "attachments",
    "audit_logs",
    "leituras_km",
    "vehicle_tracking",
    "planos_manutencao",
    "manutencoes",
    "pneus",
    "abastecimentos",
    "multas",
    "sinistros",
    "danos",
    "despesas",
    "pagamentos",
    "contrato_eventos",
    "contratos",
    "clientes",
    "veiculos",
    "usuarios",
]

# Volumes-alvo (ver docs/10-SEED-DESENVOLVIMENTO.md para o racional de cada um).
QTD_CLIENTES = 300
QTD_VEICULOS = 250
QTD_ABASTECIMENTOS = 500
QTD_MULTAS = 150
QTD_SINISTROS = 150
QTD_DANOS = 150
QTD_DESPESAS = 300


def resetar_banco(db: Session) -> None:
    print("Resetando tabelas da aplicação (TRUNCATE ... CASCADE)...")
    tabelas = ", ".join(_TABELAS_APP)
    db.execute(text(f"TRUNCATE TABLE {tabelas} RESTART IDENTITY CASCADE"))
    db.commit()


def rodar_seed(db: Session, *, com_uploads: bool) -> None:
    inicio = time.monotonic()

    print("Criando dados base...")
    usuarios = _criar_usuarios(db)
    clientes = criar_clientes(db, QTD_CLIENTES)
    veiculos, status_especiais = criar_veiculos(db, QTD_VEICULOS)

    print("Criando contratos e checklists...")
    contratos = criar_contratos(
        db, clientes, veiculos, usuarios, status_especiais, com_uploads=com_uploads
    )

    print("Criando quilometragem...")
    criar_leituras_km(db, veiculos, usuarios)
    criar_vehicle_tracking(db, veiculos)

    print("Criando manutenção e planos preventivos...")
    criar_manutencoes(db, veiculos)
    criar_planos_manutencao(db, veiculos)

    print("Criando pneus e abastecimentos...")
    criar_pneus(db, veiculos)
    criar_abastecimentos(db, veiculos, QTD_ABASTECIMENTOS)

    print("Criando multas, sinistros, danos, despesas e pagamentos...")
    criar_multas(db, veiculos, contratos, QTD_MULTAS)
    criar_sinistros(db, veiculos, contratos, QTD_SINISTROS)
    criar_danos(db, veiculos, contratos, QTD_DANOS)
    criar_despesas(db, veiculos, QTD_DESPESAS)
    criar_pagamentos(db, contratos)

    duracao = time.monotonic() - inicio
    print(f"\nSeed concluído em {duracao:.1f}s.")
    print(f"Usuários de desenvolvimento: senha 'DevSeed@123', e-mails @{DOMINIO_SEED}")


__all__ = ["resetar_banco", "rodar_seed", "usuario_seed_ja_existe"]
