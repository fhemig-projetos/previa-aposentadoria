from datetime import date, timedelta

from codigo.projecao import anos_de_dias, idade_em, projetar_data


def test_idade_em():
    assert idade_em(date(2026, 6, 14), date(1975, 6, 15)) == 50
    assert idade_em(date(2026, 6, 15), date(1975, 6, 15)) == 51


def test_anos_de_dias():
    assert anos_de_dias(365) == 0
    assert anos_de_dias(366) == 1


def test_projetar_data_encontra_primeira_data():
    alvo = date.today() + timedelta(days=30)
    assert projetar_data(lambda d: d >= alvo) == alvo


def test_projetar_data_retorna_none_alem_do_limite():
    assert projetar_data(lambda d: False) is None
