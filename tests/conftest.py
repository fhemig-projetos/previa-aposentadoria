from datetime import date

import pytest
from dateutil.relativedelta import relativedelta

from codigo.modelos import DadosTempo, Servidor


def anos_atras(anos: int, dias_extra: int = 0) -> date:
    """Data de `anos` anos (e alguns dias) atrás, para fixtures independentes do dia da execução."""
    from datetime import timedelta
    return date.today() - relativedelta(years=anos) - timedelta(days=dias_extra)


@pytest.fixture
def criar_servidor():
    def _criar(idade=40, sexo="F", anos_admissao=10):
        return Servidor(
            masp="1234567",
            adm="1",
            nome="fulana de tal",
            data_nascimento=anos_atras(idade, dias_extra=1),
            sexo=sexo,
            cargo="CARREIRA",
            funcao="categoria",
            data_admissao=anos_atras(anos_admissao),
        )
    return _criar


@pytest.fixture
def criar_tempo():
    def _criar(anos_exercicio=10, anos_externos=0, anos_cargo=None, interrupcao=False):
        anos_cargo = anos_exercicio if anos_cargo is None else anos_cargo
        return DadosTempo(
            dias_efetivo_exercicio=int(anos_exercicio * 365.25) + 1,
            dias_contribuicao_externa=int(anos_externos * 365.25) + 1 if anos_externos else 0,
            dias_no_cargo=int(anos_cargo * 365.25) + 1,
            demais_dias=0,
            dias_abono=0,
            interrupcao=interrupcao,
        )
    return _criar
