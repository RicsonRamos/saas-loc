from datetime import datetime

from pydantic import BaseModel


class LocacaoPublicaOut(BaseModel):
    em_uso: bool
    data_fim_prevista: datetime | None = None


class VeiculoPublicoOut(BaseModel):
    """Schema dedicado à rota pública (sem autenticação).

    Não reaproveita `VeiculoOut` de propósito: um campo sensível adicionado
    futuramente a `VeiculoOut` (ex. chassi, renavam, dados do cliente) não deve
    "vazar" por acidente nesta rota só por herdar o mesmo schema.
    """

    placa: str
    modelo: str
    marca: str | None
    ano: int
    status: str
    km_atual: int
    locacao_atual: LocacaoPublicaOut | None
