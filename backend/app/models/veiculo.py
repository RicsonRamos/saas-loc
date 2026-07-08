from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

STATUS_DISPONIVEL = "disponivel"
STATUS_ALUGADO = "alugado"
STATUS_RESERVADO = "reservado"
STATUS_EM_MANUTENCAO = "em_manutencao"
STATUS_SINISTRADO = "sinistrado"
STATUS_EM_LIMPEZA = "em_limpeza"
STATUS_LICENCIAMENTO_VENCIDO = "licenciamento_vencido"
STATUS_SEGURO_VENCIDO = "seguro_vencido"
STATUS_INATIVO = "inativo"

STATUS_VEICULO_VALIDOS = {
    STATUS_DISPONIVEL,
    STATUS_ALUGADO,
    STATUS_RESERVADO,
    STATUS_EM_MANUTENCAO,
    STATUS_SINISTRADO,
    STATUS_EM_LIMPEZA,
    STATUS_LICENCIAMENTO_VENCIDO,
    STATUS_SEGURO_VENCIDO,
    STATUS_INATIVO,
}

# Situações calculadas automaticamente a partir de vencimentos, nunca definidas manualmente
# (ver veiculo_service.calcular_status_efetivo). Ver docs/02-MODELO-DE-DADOS.md.
STATUS_VEICULO_AUTOMATICOS = {STATUS_LICENCIAMENTO_VENCIDO, STATUS_SEGURO_VENCIDO}


class Veiculo(TimestampedBase):
    __tablename__ = "veiculos"

    placa: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    modelo: Mapped[str] = mapped_column(String(120), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default=STATUS_DISPONIVEL)
    km_atual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    filial_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
    marca: Mapped[str | None] = mapped_column(String(60), nullable=True)
    cor: Mapped[str | None] = mapped_column(String(40), nullable=True)
    categoria: Mapped[str | None] = mapped_column(String(60), nullable=True)
    chassi: Mapped[str | None] = mapped_column(String(30), unique=True, nullable=True)
    renavam: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    combustivel: Mapped[str | None] = mapped_column(String(30), nullable=True)
    cambio: Mapped[str | None] = mapped_column(String(30), nullable=True)
    vencimento_licenciamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    vencimento_seguro: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Informações gerais (complementares)
    versao: Mapped[str | None] = mapped_column(String(60), nullable=True)
    ano_fabricacao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    portas: Mapped[int | None] = mapped_column(Integer, nullable=True)
    capacidade_passageiros: Mapped[int | None] = mapped_column(Integer, nullable=True)
    motor: Mapped[str | None] = mapped_column(String(60), nullable=True)
    potencia: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Dados de aquisição
    data_aquisicao: Mapped[date | None] = mapped_column(Date, nullable=True)
    valor_compra: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    fornecedor: Mapped[str | None] = mapped_column(String(150), nullable=True)
    forma_aquisicao: Mapped[str | None] = mapped_column(String(30), nullable=True)
    km_inicial: Mapped[int | None] = mapped_column(Integer, nullable=True)
    proprietario: Mapped[str | None] = mapped_column(String(150), nullable=True)
    data_entrada_frota: Mapped[date | None] = mapped_column(Date, nullable=True)
    garantia_fabrica_ate: Mapped[date | None] = mapped_column(Date, nullable=True)
    garantia_concessionaria_ate: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Documentação adicional
    crlv_numero: Mapped[str | None] = mapped_column(String(30), nullable=True)
    ipva_vencimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    alienado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    alienante: Mapped[str | None] = mapped_column(String(150), nullable=True)

    # Seguro detalhado (vencimento_seguro acima é a vigência final da apólice)
    seguradora: Mapped[str | None] = mapped_column(String(100), nullable=True)
    apolice_numero: Mapped[str | None] = mapped_column(String(40), nullable=True)
    seguro_franquia: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    seguro_cobertura: Mapped[str | None] = mapped_column(Text, nullable=True)
    seguro_contato: Mapped[str | None] = mapped_column(String(100), nullable=True)
