from codigo.utils.formatacao import fmt_num, fmt_tempo, formatar_chave, formatar_valor


def test_fmt_tempo():
    assert fmt_tempo(5.0) == "5 anos"
    assert fmt_tempo(1) == "1 ano"
    assert fmt_tempo(56 / 12) == "4 anos e 8 meses"
    assert fmt_tempo(4.6667) == "4 anos e 9 meses"  # meses arredondados para cima
    assert fmt_tempo(1.0833) == "1 ano e 1 mês"
    assert fmt_tempo(0) == "0 meses"


def test_fmt_tempo_sem_erro_de_ponto_flutuante():
    assert fmt_tempo(5.00000001) == "5 anos"


def test_fmt_num():
    assert fmt_num(5.0) == "5"
    assert fmt_num(4.7) == "4,7"


def test_formatar_chave_traduzida_e_generica():
    assert formatar_chave("idade_minima") == "Idade mínima"
    assert formatar_chave("alguma_chave_nova") == "Alguma chave nova"


def test_formatar_valor():
    assert formatar_valor(5.0) == 5
    assert formatar_valor(5.5) == 5.5
    assert formatar_valor("texto") == "texto"
