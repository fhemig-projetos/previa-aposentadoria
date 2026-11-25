from datetime import date

from codigo.regras import (
    RegraCompulsoria,
    RegraDireitoAdquirido,
    RegraGeral,
    RegraPontos,
)
from codigo.simulador import SimuladorAposentadoria


def test_compulsoria_cumprida(criar_servidor, criar_tempo):
    r = RegraCompulsoria().avaliar(criar_servidor(idade=76), criar_tempo())
    assert r.cumpriu
    assert r.pendencias == []
    assert r.data_previsao is None


def test_compulsoria_nao_cumprida_projeta_data(criar_servidor, criar_tempo):
    servidor = criar_servidor(idade=60)
    r = RegraCompulsoria().avaliar(servidor, criar_tempo())
    assert not r.cumpriu
    assert "15 anos" in r.pendencias[0]
    assert r.data_previsao is not None
    assert r.data_previsao.year in (date.today().year + 15, date.today().year + 14)


def test_geral_mulher_cumpre_requisitos(criar_servidor, criar_tempo):
    r = RegraGeral().avaliar(
        criar_servidor(idade=63, sexo="F"),
        criar_tempo(anos_exercicio=26, anos_cargo=10),
    )
    assert r.cumpriu
    assert r.requisitos["idade_minima"] == 62


def test_geral_homem_exige_65(criar_servidor, criar_tempo):
    r = RegraGeral().avaliar(
        criar_servidor(idade=63, sexo="M"),
        criar_tempo(anos_exercicio=26, anos_cargo=10),
    )
    assert not r.cumpriu
    assert r.requisitos["idade_minima"] == 65
    assert r.data_previsao is not None


def test_geral_lista_pendencias(criar_servidor, criar_tempo):
    r = RegraGeral().avaliar(
        criar_servidor(idade=50, sexo="F"),
        criar_tempo(anos_exercicio=5, anos_cargo=2),
    )
    assert any("idade" in p for p in r.pendencias)
    assert any("contribuição" in p for p in r.pendencias)
    assert any("serviço público" in p for p in r.pendencias)
    assert any("no cargo" in p for p in r.pendencias)


def test_pedagio_mulher(criar_servidor, criar_tempo):
    r = RegraDireitoAdquirido().avaliar(
        criar_servidor(idade=56, sexo="F"),
        criar_tempo(anos_exercicio=31, anos_cargo=21),
    )
    assert r.cumpriu
    assert r.requisitos["contribuicao_minima"] == 30
    assert r.requisitos["ingresso_maximo"] == "31/12/2003"


def test_pedagio_homem_exige_35_anos(criar_servidor, criar_tempo):
    r = RegraDireitoAdquirido().avaliar(
        criar_servidor(idade=61, sexo="M"),
        criar_tempo(anos_exercicio=31, anos_cargo=21),
    )
    assert not r.cumpriu
    assert r.requisitos["contribuicao_minima"] == 35


def test_pontos_progressao_da_pontuacao():
    regra = RegraPontos()
    assert regra._calcular_pontos_minimos("F", date(2020, 12, 31)) == 86
    assert regra._calcular_pontos_minimos("F", date(2021, 1, 1)) == 86
    assert regra._calcular_pontos_minimos("F", date(2022, 4, 1)) == 87   # +15 meses
    assert regra._calcular_pontos_minimos("M", date(2021, 1, 1)) == 97
    assert regra._calcular_pontos_minimos("F", date(2100, 1, 1)) == 100  # limite
    assert regra._calcular_pontos_minimos("M", date(2100, 1, 1)) == 105  # limite


def test_pontos_reducao_idade_exige_ingresso_ate_1998_sem_interrupcao(
    criar_servidor, criar_tempo
):
    regra = RegraPontos()
    servidor = criar_servidor(idade=55, anos_admissao=40)  # ingresso < 1998
    tempo = criar_tempo(anos_exercicio=40, interrupcao=True)

    assert regra._calcular_reducao_idade_minima(servidor, tempo, 30) > 0

    tempo.interrupcao = False
    assert regra._calcular_reducao_idade_minima(servidor, tempo, 30) == 0

    servidor.data_admissao = date(2005, 1, 1)
    tempo.interrupcao = True
    assert regra._calcular_reducao_idade_minima(servidor, tempo, 30) == 0


def test_pontos_cumprida(criar_servidor, criar_tempo):
    r = RegraPontos().avaliar(
        criar_servidor(idade=62, sexo="F"),
        criar_tempo(anos_exercicio=38, anos_cargo=20),
    )
    assert r.cumpriu
    assert r.valores_apurados["somatorio_pontos"] >= r.requisitos["pontos_minimos"]


def test_simulador_executa_todas_as_regras(criar_servidor, criar_tempo):
    resultados = SimuladorAposentadoria().simular(
        criar_servidor(), criar_tempo()
    )
    assert [r.codigo for r in resultados] == [
        "DA_EC104", "REGRA_GERAL", "REGRA_COMPULSORIA", "REGRA_PONTOS",
    ]
