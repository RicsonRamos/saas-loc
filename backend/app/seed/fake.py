"""Instância Faker compartilhada e geradores customizados para campos que o Faker
não cobre nativamente (placa, chassi, RENAVAM) — com deduplicação para os campos
`unique` do banco (documento, placa, chassi, renavam, email).
"""

import random
import string
from collections.abc import Callable, Iterable
from typing import TypeVar

from faker import Faker

fake = Faker("pt_BR")
Faker.seed(42)
random.seed(42)

T = TypeVar("T")


def unico(gerador: Callable[[], T], usados: set[T], tentativas: int = 100) -> T:
    """Chama `gerador()` até obter um valor ainda não presente em `usados`."""
    for _ in range(tentativas):
        valor = gerador()
        if valor not in usados:
            usados.add(valor)
            return valor
    raise RuntimeError(f"Não foi possível gerar valor único após {tentativas} tentativas.")


def escolher(opcoes: Iterable[T]) -> T:
    return random.choice(list(opcoes))


def gerar_placa() -> str:
    """Formato antigo (ABC1234) ou Mercosul (ABC1D23), aleatoriamente."""
    letras = "".join(random.choices(string.ascii_uppercase, k=3))
    if random.random() < 0.5:
        return f"{letras}{random.randint(1000, 9999)}"
    letra_extra = random.choice(string.ascii_uppercase)
    return f"{letras}{random.randint(1, 9)}{letra_extra}{random.randint(10, 99)}"


def gerar_chassi() -> str:
    """VIN-like: 17 caracteres alfanuméricos maiúsculos (sem I/O/Q, como no padrão real)."""
    alfabeto = "".join(c for c in string.ascii_uppercase + string.digits if c not in "IOQ")
    return "".join(random.choices(alfabeto, k=17))


def gerar_renavam() -> str:
    return "".join(random.choices(string.digits, k=11))


def gerar_documento() -> str:
    return fake.cnpj() if random.random() < 0.15 else fake.cpf()
