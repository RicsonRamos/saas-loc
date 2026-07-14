from datetime import UTC, date, datetime, time, timedelta

from sqlalchemy.orm import Session

from app.models.manutencao import Manutencao
from app.models.plano_manutencao import TIPOS_PLANO_MANUTENCAO_VALIDOS, PlanoManutencao
from app.models.veiculo import Veiculo
from app.schemas.manutencao import ManutencaoCreate
from app.schemas.plano_manutencao import PlanoManutencaoCreate
from app.seed.fake import escolher, fake

_OFICINAS = ["Oficina Central", "Auto Center Norte", "Mecânica São José", "Speed Motors"]

# intervalos típicos por tipo de plano de manutenção (km, dias) — usados tanto para
# gerar o plano quanto para calcular quanto "usar" do intervalo por cenário.
_INTERVALOS_POR_TIPO: dict[str, tuple[int | None, int | None]] = {
    "troca_oleo": (5000, None),
    "troca_filtros": (10000, None),
    "pastilhas_freio": (25000, None),
    "pneus": (40000, None),
    "revisao": (10000, 365),
    "alinhamento_balanceamento": (15000, None),
    "licenciamento": (None, 365),
    "seguro": (None, 365),
}


def criar_manutencoes(db: Session, veiculos: list[Veiculo]) -> int:
    """Insere as manutenções em lote (bypassa `manutencao_service.registrar`, que só
    faz insert + efeito colateral em `veiculo.km_atual`/`status` — replicado aqui
    direto nos objetos `Veiculo` já carregados na sessão, sem round trip extra)."""
    hoje = datetime.now(UTC).date()
    manutencoes: list[Manutencao] = []

    for veiculo in veiculos:
        n = escolher([0, 1, 1, 1, 2])
        for _ in range(n):
            tipo = escolher(["preventiva", "corretiva"])
            data = datetime.combine(
                hoje - timedelta(days=fake.random_int(5, 500)), time(14, 0), tzinfo=UTC
            )
            km_na_epoca = max(0, veiculo.km_atual - fake.random_int(0, 15000))

            cenario = escolher(["atrasada", "futura", "sem_proxima"])
            proxima_km = None
            proxima_data = None
            if cenario == "atrasada":
                proxima_km = max(0, veiculo.km_atual - fake.random_int(100, 2000))
                proxima_data = hoje - timedelta(days=fake.random_int(1, 60))
            elif cenario == "futura":
                proxima_km = veiculo.km_atual + fake.random_int(500, 8000)
                proxima_data = hoje + timedelta(days=fake.random_int(10, 200))

            payload = ManutencaoCreate(
                veiculo_id=veiculo.id,
                tipo=tipo,
                data=data,
                km=km_na_epoca,
                custo=fake.random_int(80, 2500),
                oficina=escolher(_OFICINAS),
                descricao=escolher(
                    [None, "Revisão de rotina", "Troca de peça desgastada", "Reparo pós-uso"]
                ),
                proxima_manutencao_km=proxima_km,
                proxima_manutencao_data=proxima_data,
            )
            manutencoes.append(Manutencao(**payload.model_dump(exclude={"em_andamento"})))

            # Mesma condição de manutencao_service.registrar: km_na_epoca nunca
            # ultrapassa veiculo.km_atual pela fórmula acima, mas mantém a checagem
            # para ficar fiel ao efeito colateral do service caso isso mude.
            if payload.km > veiculo.km_atual:
                veiculo.km_atual = payload.km

    db.add_all(manutencoes)
    db.commit()
    print(f"  manutencoes: {len(manutencoes)} criadas")
    return len(manutencoes)


def _ultima_execucao_para_cenario(
    veiculo_km_atual: int,
    hoje: date,
    intervalo_km: int | None,
    intervalo_dias: int | None,
    cenario: str,
) -> tuple[int | None, date | None]:
    """Escolhe ultima_execucao_km/data para que o plano caia deliberadamente em
    normal/atencao/critico, replicando a fórmula de plano_manutencao_service.calcular_status."""
    fracoes = {"normal": 0.3, "atencao": 0.9, "critico": 1.15}
    fracao = fracoes[cenario]

    ultima_km = None
    ultima_data = None
    if intervalo_km is not None:
        consumido = round(intervalo_km * fracao)
        ultima_km = max(0, veiculo_km_atual - consumido)
    if intervalo_dias is not None:
        consumido_dias = round(intervalo_dias * fracao)
        ultima_data = hoje - timedelta(days=consumido_dias)
    return ultima_km, ultima_data


def criar_planos_manutencao(db: Session, veiculos: list[Veiculo]) -> int:
    """Insere os planos em lote (bypassa `plano_manutencao_service.criar`, que só faz
    insert simples sem efeito colateral em outra tabela)."""
    hoje = datetime.now(UTC).date()
    planos: list[PlanoManutencao] = []

    for veiculo in veiculos:
        if fake.random.random() < 0.4:
            continue  # ~40% dos veículos sem nenhum plano configurado ainda

        tipos = fake.random.sample(
            sorted(TIPOS_PLANO_MANUTENCAO_VALIDOS - {"outro"}),
            k=fake.random_int(1, 3),
        )
        for tipo in tipos:
            intervalo_km, intervalo_dias = _INTERVALOS_POR_TIPO[tipo]
            cenario = escolher(["normal", "normal", "atencao", "critico"])
            ultima_km, ultima_data = _ultima_execucao_para_cenario(
                veiculo.km_atual, hoje, intervalo_km, intervalo_dias, cenario
            )
            payload = PlanoManutencaoCreate(
                veiculo_id=veiculo.id,
                tipo=tipo,
                intervalo_km=intervalo_km,
                intervalo_dias=intervalo_dias,
                ultima_execucao_km=ultima_km,
                ultima_execucao_data=ultima_data,
            )
            planos.append(PlanoManutencao(**payload.model_dump()))

    db.add_all(planos)
    db.commit()
    print(f"  planos_manutencao: {len(planos)} criados")
    return len(planos)
