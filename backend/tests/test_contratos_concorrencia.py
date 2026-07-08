"""O teste não-negociável do projeto: ver docs/08-TESTES-QUALIDADE.md.

Duas requisições concorrentes tentando reservar o mesmo veículo no mesmo período —
apenas uma pode vencer. Isso é verificado contra o banco real (constraint de exclusão
`contratos_sem_overlap`), usando duas conexões/threads independentes, não apenas
validação em Python.
"""

import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.models.cliente import Cliente
from app.models.contrato import STATUS_ATIVO, Contrato, ContratoEvento
from app.models.veiculo import Veiculo


def _preparar_cliente_e_veiculo(engine) -> tuple:
    """Cria dados próprios da chamada (placa/documento únicos) e commita de verdade,
    pois o teste de concorrência precisa de linhas visíveis a múltiplas conexões reais —
    diferente de `db_session`, que roda tudo em uma transação desfeita ao final."""
    sufixo = uuid.uuid4().hex[:6].upper()
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    cliente = Cliente(nome="Cliente Concorrência", documento=f"999{sufixo}")
    veiculo = Veiculo(placa=f"CC{sufixo}", modelo="Concorrencia", ano=2024)
    session.add_all([cliente, veiculo])
    session.commit()
    cliente_id, veiculo_id = cliente.id, veiculo.id
    session.close()
    return cliente_id, veiculo_id


def _limpar(engine, cliente_id, veiculo_id) -> None:
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    session.query(ContratoEvento).filter(
        ContratoEvento.contrato_id.in_(
            session.query(Contrato.id).filter(Contrato.veiculo_id == veiculo_id)
        )
    ).delete(synchronize_session=False)
    session.query(Contrato).filter(Contrato.veiculo_id == veiculo_id).delete(
        synchronize_session=False
    )
    session.query(Veiculo).filter(Veiculo.id == veiculo_id).delete(synchronize_session=False)
    session.query(Cliente).filter(Cliente.id == cliente_id).delete(synchronize_session=False)
    session.commit()
    session.close()


def _tentar_reservar(engine, cliente_id, veiculo_id, inicio, fim) -> str:
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        contrato = Contrato(
            cliente_id=cliente_id,
            veiculo_id=veiculo_id,
            data_inicio=inicio,
            data_fim_prevista=fim,
            valor_diaria=Decimal("100.00"),
            status=STATUS_ATIVO,
        )
        session.add(contrato)
        session.commit()
        return "sucesso"
    except IntegrityError:
        session.rollback()
        return "conflito"
    finally:
        session.close()


def test_duas_reservas_simultaneas_para_o_mesmo_veiculo_apenas_uma_vence(engine):
    cliente_id, veiculo_id = _preparar_cliente_e_veiculo(engine)
    inicio = datetime(2026, 9, 1, tzinfo=UTC)
    fim = datetime(2026, 9, 5, tzinfo=UTC)

    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            futuros = [
                executor.submit(_tentar_reservar, engine, cliente_id, veiculo_id, inicio, fim)
                for _ in range(2)
            ]
            resultados = [futuro.result() for futuro in futuros]

        assert resultados.count("sucesso") == 1
        assert resultados.count("conflito") == 1
    finally:
        _limpar(engine, cliente_id, veiculo_id)


def test_periodos_nao_sobrepostos_nao_geram_conflito(engine):
    cliente_id, veiculo_id = _preparar_cliente_e_veiculo(engine)

    try:
        resultado_1 = _tentar_reservar(
            engine,
            cliente_id,
            veiculo_id,
            datetime(2026, 10, 1, tzinfo=UTC),
            datetime(2026, 10, 5, tzinfo=UTC),
        )
        resultado_2 = _tentar_reservar(
            engine,
            cliente_id,
            veiculo_id,
            datetime(2026, 10, 6, tzinfo=UTC),
            datetime(2026, 10, 10, tzinfo=UTC),
        )

        assert resultado_1 == "sucesso"
        assert resultado_2 == "sucesso"
    finally:
        _limpar(engine, cliente_id, veiculo_id)
