import uuid
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, VeiculoIndisponivelError
from app.models.cliente import Cliente
from app.models.contrato import STATUS_RESERVADO, Contrato, ContratoEvento
from app.models.usuario import Usuario
from app.models.veiculo import (
    STATUS_EM_MANUTENCAO,
    STATUS_INATIVO,
    Veiculo,
)
from app.models.veiculo import (
    STATUS_RESERVADO as VEICULO_RESERVADO,
)
from app.schemas.contrato import ContratoCreate, ContratoDevolucao
from app.seed.checklists import criar_checklist_devolucao, criar_checklist_entrega
from app.seed.fake import escolher, fake
from app.services import contrato_service

_STATUS_ESPECIAIS_BLOQUEIAM_LOCACAO = {STATUS_EM_MANUTENCAO, STATUS_INATIVO}


def _km_interpolado(km_base: int, km_alvo: int, entrada: date, hoje: date, na_data: date) -> int:
    dias_totais = max((hoje - entrada).days, 1)
    fracao = min(max((na_data - entrada).days / dias_totais, 0.0), 1.0)
    return km_base + round((km_alvo - km_base) * fracao)


def _gerar_historico(
    db: Session,
    veiculo: Veiculo,
    km_alvo_hoje: int,
    clientes: list[Cliente],
    usuarios: list[Usuario],
    hoje: date,
    com_uploads: bool,
) -> None:
    entrada = veiculo.data_entrada_frota or (hoje - timedelta(days=365))
    km_base = veiculo.km_inicial or 0
    cursor = datetime.combine(entrada, time(9, 0), tzinfo=UTC)
    n_historicos = escolher([0, 1, 1, 2])

    for _ in range(n_historicos):
        cursor = cursor + timedelta(days=fake.random_int(2, 25))
        duracao = fake.random_int(2, 20)
        data_inicio = cursor
        data_fim_prevista = data_inicio + timedelta(days=duracao)
        if data_fim_prevista.date() >= hoje - timedelta(days=5):
            break

        km_inicio = _km_interpolado(km_base, km_alvo_hoje, entrada, hoje, data_inicio.date())
        km_fim = km_inicio + fake.random_int(50, duracao * 300)
        usuario = escolher(usuarios)

        try:
            contrato = contrato_service.criar_locacao(
                db,
                ContratoCreate(
                    cliente_id=escolher(clientes).id,
                    veiculo_id=veiculo.id,
                    data_inicio=data_inicio,
                    data_fim_prevista=data_fim_prevista,
                    valor_diaria=Decimal(fake.random_int(80, 350)),
                    km_inicio=km_inicio,
                    km_contratado_mensal=escolher([None, None, None, 800, 1000, 1500]),
                ),
                usuario_id=usuario.id,
            )
        except (ConflictError, VeiculoIndisponivelError):
            cursor = data_fim_prevista
            continue

        if fake.random.random() < 0.1:
            contrato_service.cancelar(db, contrato.id, usuario_id=usuario.id)
        else:
            tem_entrega = fake.random.random() < 0.9
            if tem_entrega:
                criar_checklist_entrega(db, contrato, km_inicio, usuarios, com_uploads)
            # ~35% dos contratos encerrados (com entrega) ficam de propósito sem
            # checklist de devolução — a devolução exige entrega prévia registrada.
            if tem_entrega and fake.random.random() < 0.65:
                atrasado = fake.random.random() < 0.15
                delta_dias = fake.random_int(1, 4) if atrasado else -fake.random_int(0, 1)
                data_fim_real = data_fim_prevista + timedelta(days=delta_dias)
                criar_checklist_devolucao(
                    db, contrato, km_fim, data_fim_real, usuarios, com_uploads
                )
            else:
                data_fim_real = data_fim_prevista
            contrato_service.devolver(
                db,
                contrato.id,
                ContratoDevolucao(data_fim_real=data_fim_real, km_final=km_fim),
                usuario_id=usuario.id,
            )
        cursor = data_fim_prevista


def _criar_reserva_futura(
    db: Session, veiculo: Veiculo, clientes: list[Cliente], hoje: date
) -> None:
    """Insere um contrato "reservado" diretamente via ORM: o service atual sempre
    cria contratos já como "ativo" (não há fluxo de reserva-para-depois na API hoje),
    então uma reserva futura de verdade só é possível inserindo o registro direto."""
    data_inicio = datetime.combine(
        hoje + timedelta(days=fake.random_int(3, 20)), time(10, 0), tzinfo=UTC
    )
    duracao = fake.random_int(2, 15)
    contrato = Contrato(
        id=uuid.uuid4(),
        cliente_id=escolher(clientes).id,
        veiculo_id=veiculo.id,
        data_inicio=data_inicio,
        data_fim_prevista=data_inicio + timedelta(days=duracao),
        valor_diaria=Decimal(fake.random_int(80, 350)),
        km_contratado_mensal=escolher([None, 800, 1000]),
        status=STATUS_RESERVADO,
    )
    db.add(contrato)
    db.flush()
    db.add(
        ContratoEvento(contrato_id=contrato.id, status_anterior=None, status_novo=STATUS_RESERVADO)
    )
    veiculo.status = VEICULO_RESERVADO
    db.commit()


def criar_contratos(
    db: Session,
    clientes: list[Cliente],
    veiculos: list[Veiculo],
    usuarios: list[Usuario],
    status_especiais: dict[uuid.UUID, str],
    com_uploads: bool = False,
) -> list[Contrato]:
    hoje = datetime.now(UTC).date()
    total_criados = 0

    for veiculo in veiculos:
        km_alvo = veiculo.km_atual
        _gerar_historico(db, veiculo, km_alvo, clientes, usuarios, hoje, com_uploads)
        total_criados += 1

        if veiculo.id in status_especiais:
            # Histórico pode ter deixado o veículo como "disponível" (efeito colateral
            # de devolver()/cancelar()) — reaplica o status especial definido na fase
            # de veículos, que não depende de contrato.
            veiculo.status = status_especiais[veiculo.id]
            db.commit()
            continue

        r = fake.random.random()
        if r < 0.35:
            data_inicio = datetime.combine(
                hoje - timedelta(days=fake.random_int(0, 10)), time(9, 0), tzinfo=UTC
            )
            vence_em_breve = fake.random.random() < 0.4
            duracao = fake.random_int(1, 5) if vence_em_breve else fake.random_int(5, 20)
            km_contratado_baixo = fake.random.random() < 0.25
            usuario = escolher(usuarios)
            try:
                contrato_atual = contrato_service.criar_locacao(
                    db,
                    ContratoCreate(
                        cliente_id=escolher(clientes).id,
                        veiculo_id=veiculo.id,
                        data_inicio=data_inicio,
                        data_fim_prevista=data_inicio + timedelta(days=duracao),
                        valor_diaria=Decimal(fake.random_int(80, 350)),
                        km_inicio=veiculo.km_atual,
                        km_contratado_mensal=300 if km_contratado_baixo else escolher(
                            [None, 1000, 1500, 2000]
                        ),
                    ),
                    usuario_id=usuario.id,
                )
                if km_contratado_baixo:
                    veiculo.km_atual += fake.random_int(400, 2500)
                    db.commit()
                if fake.random.random() < 0.85:
                    criar_checklist_entrega(
                        db, contrato_atual, contrato_atual.km_inicio, usuarios, com_uploads
                    )
            except (ConflictError, VeiculoIndisponivelError):
                pass
        elif r < 0.5:
            _criar_reserva_futura(db, veiculo, clientes, hoje)

    contratos = list(db.execute(select(Contrato)).scalars().all())
    print(f"  contratos: {len(contratos)} (processados {total_criados} veículos)")
    return contratos
