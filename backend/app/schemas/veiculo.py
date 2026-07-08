from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.veiculo import STATUS_VEICULO_VALIDOS
from app.schemas.dano import DanoOut
from app.schemas.multa import MultaOut
from app.schemas.sinistro import SinistroOut


class VeiculoCreate(BaseModel):
    placa: str = Field(min_length=7, max_length=10)
    modelo: str = Field(min_length=1, max_length=120)
    ano: int = Field(ge=1950, le=2100)
    km_atual: int = Field(default=0, ge=0)
    filial_id: str | None = None
    marca: str | None = Field(default=None, max_length=60)
    cor: str | None = Field(default=None, max_length=40)
    categoria: str | None = Field(default=None, max_length=60)
    chassi: str | None = Field(default=None, max_length=30)
    renavam: str | None = Field(default=None, max_length=20)
    combustivel: str | None = Field(default=None, max_length=30)
    cambio: str | None = Field(default=None, max_length=30)
    vencimento_licenciamento: date | None = None
    vencimento_seguro: date | None = None

    versao: str | None = Field(default=None, max_length=60)
    ano_fabricacao: int | None = Field(default=None, ge=1950, le=2100)
    portas: int | None = Field(default=None, ge=0, le=10)
    capacidade_passageiros: int | None = Field(default=None, ge=0, le=100)
    motor: str | None = Field(default=None, max_length=60)
    potencia: str | None = Field(default=None, max_length=30)

    data_aquisicao: date | None = None
    valor_compra: Decimal | None = Field(default=None, ge=0)
    fornecedor: str | None = Field(default=None, max_length=150)
    forma_aquisicao: str | None = Field(default=None, max_length=30)
    km_inicial: int | None = Field(default=None, ge=0)
    proprietario: str | None = Field(default=None, max_length=150)
    data_entrada_frota: date | None = None
    garantia_fabrica_ate: date | None = None
    garantia_concessionaria_ate: date | None = None

    crlv_numero: str | None = Field(default=None, max_length=30)
    ipva_vencimento: date | None = None
    alienado: bool = False
    alienante: str | None = Field(default=None, max_length=150)

    seguradora: str | None = Field(default=None, max_length=100)
    apolice_numero: str | None = Field(default=None, max_length=40)
    seguro_franquia: Decimal | None = Field(default=None, ge=0)
    seguro_cobertura: str | None = None
    seguro_contato: str | None = Field(default=None, max_length=100)

    @field_validator("placa")
    @classmethod
    def placa_maiuscula(cls, v: str) -> str:
        return v.strip().upper()


class VeiculoUpdate(BaseModel):
    modelo: str | None = Field(default=None, max_length=120)
    ano: int | None = Field(default=None, ge=1950, le=2100)
    km_atual: int | None = Field(default=None, ge=0)
    status: str | None = None
    filial_id: str | None = None
    marca: str | None = Field(default=None, max_length=60)
    cor: str | None = Field(default=None, max_length=40)
    categoria: str | None = Field(default=None, max_length=60)
    chassi: str | None = Field(default=None, max_length=30)
    renavam: str | None = Field(default=None, max_length=20)
    combustivel: str | None = Field(default=None, max_length=30)
    cambio: str | None = Field(default=None, max_length=30)
    vencimento_licenciamento: date | None = None
    vencimento_seguro: date | None = None

    versao: str | None = Field(default=None, max_length=60)
    ano_fabricacao: int | None = Field(default=None, ge=1950, le=2100)
    portas: int | None = Field(default=None, ge=0, le=10)
    capacidade_passageiros: int | None = Field(default=None, ge=0, le=100)
    motor: str | None = Field(default=None, max_length=60)
    potencia: str | None = Field(default=None, max_length=30)

    data_aquisicao: date | None = None
    valor_compra: Decimal | None = Field(default=None, ge=0)
    fornecedor: str | None = Field(default=None, max_length=150)
    forma_aquisicao: str | None = Field(default=None, max_length=30)
    km_inicial: int | None = Field(default=None, ge=0)
    proprietario: str | None = Field(default=None, max_length=150)
    data_entrada_frota: date | None = None
    garantia_fabrica_ate: date | None = None
    garantia_concessionaria_ate: date | None = None

    crlv_numero: str | None = Field(default=None, max_length=30)
    ipva_vencimento: date | None = None
    alienado: bool | None = None
    alienante: str | None = Field(default=None, max_length=150)

    seguradora: str | None = Field(default=None, max_length=100)
    apolice_numero: str | None = Field(default=None, max_length=40)
    seguro_franquia: Decimal | None = Field(default=None, ge=0)
    seguro_cobertura: str | None = None
    seguro_contato: str | None = Field(default=None, max_length=100)

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUS_VEICULO_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_VEICULO_VALIDOS)}")
        return v


class VeiculoOut(BaseModel):
    id: UUID
    placa: str
    codigo_publico: str
    modelo: str
    ano: int
    status: str
    km_atual: int
    filial_id: str | None
    marca: str | None
    cor: str | None
    categoria: str | None
    chassi: str | None
    renavam: str | None
    combustivel: str | None
    cambio: str | None
    vencimento_licenciamento: date | None
    vencimento_seguro: date | None

    versao: str | None
    ano_fabricacao: int | None
    portas: int | None
    capacidade_passageiros: int | None
    motor: str | None
    potencia: str | None

    data_aquisicao: date | None
    valor_compra: Decimal | None
    fornecedor: str | None
    forma_aquisicao: str | None
    km_inicial: int | None
    proprietario: str | None
    data_entrada_frota: date | None
    garantia_fabrica_ate: date | None
    garantia_concessionaria_ate: date | None

    crlv_numero: str | None
    ipva_vencimento: date | None
    alienado: bool
    alienante: str | None

    seguradora: str | None
    apolice_numero: str | None
    seguro_franquia: Decimal | None
    seguro_cobertura: str | None
    seguro_contato: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HistoricoContratoOut(BaseModel):
    id: UUID
    cliente_id: UUID
    cliente_nome: str
    data_inicio: datetime
    data_fim_prevista: datetime
    data_fim_real: datetime | None
    status: str
    valor_diaria: Decimal
    km_inicio: int | None
    km_final: int | None


class HistoricoManutencaoOut(BaseModel):
    id: UUID
    tipo: str
    data: datetime
    km: int
    custo: Decimal
    oficina: str | None

    model_config = ConfigDict(from_attributes=True)


class HistoricoDespesaOut(BaseModel):
    id: UUID
    categoria: str
    valor: Decimal
    data: datetime
    descricao: str | None

    model_config = ConfigDict(from_attributes=True)


class EventoKmOut(BaseModel):
    data: datetime
    km: int
    origem: str
    descricao: str


class IndicadoresVeiculoOut(BaseModel):
    receita_total: Decimal
    custo_total: Decimal
    lucro: Decimal
    custo_por_km: Decimal | None
    dias_desde_entrada: int
    dias_locado: int
    dias_parado: int
    taxa_utilizacao: Decimal


class HistoricoVeiculoOut(BaseModel):
    contratos: list[HistoricoContratoOut]
    manutencoes: list[HistoricoManutencaoOut]
    despesas: list[HistoricoDespesaOut]
    multas: list[MultaOut]
    sinistros: list[SinistroOut]
    danos: list[DanoOut]
    eventos_km: list[EventoKmOut]
    indicadores: IndicadoresVeiculoOut
