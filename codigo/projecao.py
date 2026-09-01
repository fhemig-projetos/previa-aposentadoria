"""Projeção da data em que os requisitos de cada regra serão atendidos.

A projeção parte da premissa simplificada de acúmulo contínuo de 1 dia de
tempo para cada dia corrido (servidor permanece em exercício), sem novos
períodos de interrupção.
"""

import math
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

DIAS_POR_ANO = 365.25
LIMITE_ANOS = 100


def idade_em(data_referencia: date, data_nascimento: date) -> int:
    """Idade (anos completos) do servidor em uma determinada data."""
    return relativedelta(data_referencia, data_nascimento).years


def anos_de_dias(dias: int) -> int:
    """Converte dias em anos usando o mesmo critério do DadosTempo."""
    return math.floor(dias / DIAS_POR_ANO)


def projetar_data(condicao) -> date | None:
    """Retorna a primeira data, a partir de hoje, em que ``condicao`` é atendida.

    Parâmetros
    ----------
    condicao : callable
        Função que recebe uma ``datetime.date`` e devolve ``bool``.

    Retorna ``None`` se a condição não for satisfeita dentro do limite
    (``LIMITE_ANOS`` anos).
    """
    hoje = date.today()
    limite_dias = LIMITE_ANOS * DIAS_POR_ANO

    data = hoje
    while not condicao(data):
        data += timedelta(days=1)
        if (data - hoje).days > limite_dias:
            return None
    return data