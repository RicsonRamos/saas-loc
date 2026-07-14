from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.veiculo import (
    STATUS_EM_LIMPEZA,
    STATUS_EM_MANUTENCAO,
    STATUS_INATIVO,
    STATUS_SINISTRADO,
    Veiculo,
)
from app.schemas.veiculo import VeiculoCreate
from app.seed.fake import escolher, fake, gerar_chassi, gerar_placa, gerar_renavam, unico

# (marca, [modelos], categoria) — catálogo pequeno e realista de frota de locadora.
_CATALOGO = [
    ("Chevrolet", ["Onix", "Onix Plus", "Tracker", "Spin"], "hatch"),
    ("Volkswagen", ["Gol", "Polo", "T-Cross", "Virtus"], "hatch"),
    ("Fiat", ["Mobi", "Argo", "Pulse", "Strada"], "economico"),
    ("Hyundai", ["HB20", "Creta", "HB20S"], "hatch"),
    ("Toyota", ["Corolla", "Yaris", "Corolla Cross"], "sedan"),
    ("Honda", ["City", "Civic", "HR-V"], "sedan"),
    ("Jeep", ["Renegade", "Compass"], "suv"),
    ("Renault", ["Kwid", "Sandero", "Duster"], "economico"),
]

_CORES = ["Branco", "Prata", "Preto", "Cinza", "Vermelho", "Azul"]
_COMBUSTIVEIS = ["flex", "gasolina", "diesel", "hibrido"]
_CAMBIOS = ["manual", "automatico", "cvt"]

def _status_diretamente_atribuiveis(quantidade: int) -> list[str]:
    """~28% dos veículos recebem um status que não depende de contrato/manutenção
    futura (o restante fica "disponível" para a fase de contratos alugar/reservar)."""
    return (
        [STATUS_EM_MANUTENCAO] * max(1, round(quantidade * 0.08))
        + [STATUS_SINISTRADO] * max(1, round(quantidade * 0.04))
        + [STATUS_EM_LIMPEZA] * max(1, round(quantidade * 0.06))
        + [STATUS_INATIVO] * max(1, round(quantidade * 0.05))
    )


def _gerar_veiculo_create(hoje: date, usados: dict[str, set[str]]) -> VeiculoCreate:
    marca, modelos, categoria = escolher(_CATALOGO)
    modelo = escolher(modelos)
    ano_fabricacao = fake.random_int(hoje.year - 8, hoje.year)
    recem_adquirido = fake.random.random() < 0.1
    alta_quilometragem = fake.random.random() < 0.12

    if recem_adquirido:
        data_entrada = hoje - timedelta(days=fake.random_int(1, 30))
        km_inicial = 0
        km_atual = fake.random_int(0, 500)
    elif alta_quilometragem:
        data_entrada = hoje - timedelta(days=fake.random_int(700, 365 * 6))
        km_inicial = 0
        km_atual = fake.random_int(90000, 180000)
    else:
        data_entrada = hoje - timedelta(days=fake.random_int(60, 700))
        km_inicial = 0
        km_atual = fake.random_int(3000, 60000)

    vencimento_licenciamento = hoje + timedelta(days=fake.random_int(-60, 400))
    vencimento_seguro = hoje + timedelta(days=fake.random_int(-30, 400))

    return VeiculoCreate(
        placa=unico(gerar_placa, usados["placa"]),
        modelo=modelo,
        ano=ano_fabricacao,
        km_atual=km_atual,
        marca=marca,
        cor=escolher(_CORES),
        categoria=categoria,
        chassi=unico(gerar_chassi, usados["chassi"]),
        renavam=unico(gerar_renavam, usados["renavam"]),
        combustivel=escolher(_COMBUSTIVEIS),
        cambio=escolher(_CAMBIOS),
        vencimento_licenciamento=vencimento_licenciamento,
        vencimento_seguro=vencimento_seguro,
        ano_fabricacao=ano_fabricacao,
        portas=escolher([2, 4]),
        capacidade_passageiros=escolher([4, 5, 7]),
        motor=escolher(["1.0", "1.3", "1.6", "2.0"]),
        data_aquisicao=data_entrada,
        valor_compra=Decimal(fake.random_int(45000, 160000)),
        fornecedor=fake.company(),
        forma_aquisicao=escolher(["compra_direta", "financiamento", "consorcio"]),
        km_inicial=km_inicial,
        proprietario="Locadora Frota Própria",
        data_entrada_frota=data_entrada,
        crlv_numero=fake.numerify("##########"),
        ipva_vencimento=hoje + timedelta(days=fake.random_int(-30, 300)),
        alienado=fake.random.random() < 0.2,
        seguradora=escolher(["Porto Seguro", "Azul Seguros", "Allianz", "HDI"]),
        apolice_numero=fake.numerify("APL-########"),
        seguro_franquia=Decimal(fake.random_int(1500, 6000)),
        seguro_contato=fake.phone_number(),
    )


def criar_veiculos(db: Session, quantidade: int) -> tuple[list[Veiculo], dict]:
    """Retorna (veiculos, status_especiais) — o segundo é um dict veiculo_id -> status
    para os veículos cujo status não deve ser derivado de contrato (em_manutencao,
    sinistrado, em_limpeza, inativo), usado pela fase de contratos para reaplicar
    esse status caso o histórico de locações o tenha sobrescrito.

    Insere em lote (bypassa `veiculo_service.criar`/`atualizar`, que só fazem
    insert/setattr simples sem efeito colateral em outra tabela — ver
    docs/10-SEED-DESENVOLVIMENTO.md)."""
    hoje = date.today()
    usados: dict[str, set[str]] = {"placa": set(), "chassi": set(), "renavam": set()}
    veiculos: list[Veiculo] = []

    for _ in range(quantidade):
        payload = _gerar_veiculo_create(hoje, usados)
        veiculos.append(Veiculo(**payload.model_dump()))

    db.add_all(veiculos)
    db.flush()  # popula veiculo.id (default client-side, só existe após o flush)

    candidatos = list(veiculos)
    fake.random.shuffle(candidatos)
    status_especiais: dict = {}
    for veiculo, status in zip(
        candidatos, _status_diretamente_atribuiveis(quantidade), strict=False
    ):
        veiculo.status = status
        status_especiais[veiculo.id] = status

    db.commit()

    print(f"  veiculos: {len(veiculos)} criados ({len(status_especiais)} com status especial)")
    return veiculos, status_especiais
