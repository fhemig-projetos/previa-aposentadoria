"""Funções de formatação usadas pelas regras, pela interface e pelo PDF."""

import math

TRADUCOES_CHAVES = {
    "idade": "Idade",
    "anos_efetivo_exercicio": "Anos de efetivo exercício",
    "anos_contribuicao_externa": "Anos de contribuição externa",
    "anos_total_contribuicao": "Tempo total de contribuição",
    "anos_no_cargo": "Anos no cargo",
    "anos_na_carreira": "Anos na carreira",
    "idade_minima": "Idade mínima",
    "contribuicao_minima": "Tempo mínimo de contribuição",
    "servico_publico_minimo": "Tempo mínimo de serviço público",
    "carreira_minima": "Tempo mínimo na carreira",
    "cargo_minimo": "Tempo mínimo no cargo",
    "data_limite_ingresso": "Data limite de ingresso no serviço público",
    "idade_compulsoria": "Idade para aposentadoria compulsória",
    "ingresso_maximo": "Data máxima de ingresso",
    "data_admissao": "Data de admissão",
    "pontos_minimos": "Pontuação mínima",
    "somatorio_pontos": "Somatório de pontos",
    "idade_minima_efetiva": "Idade mínima efetiva",
}


def fmt_num(valor, casas: int = 1) -> str:
    """Mostra inteiro sem '.0' (5.0 -> '5') e decimal com vírgula (4.7 -> '4,7')."""
    valor = round(float(valor), casas)
    if valor.is_integer():
        return str(int(valor))
    return f"{valor:.{casas}f}".replace(".", ",")


def fmt_tempo(anos) -> str:
    """Converte anos decimais em 'X anos e Y meses'.

    5.0 -> '5 anos' | 56/12 -> '4 anos e 8 meses' | 1.0833 -> '1 ano e 1 mês'
    Os meses são arredondados para cima (4.6667 -> '4 anos e 9 meses').
    """
    # round(..., 6) evita erro de ponto flutuante (ex.: 60.00000001 meses)
    total_meses = math.ceil(round(float(anos) * 12, 6))
    a, m = divmod(total_meses, 12)
    partes = []
    if a:
        partes.append(f"{a} {'ano' if a == 1 else 'anos'}")
    if m:
        partes.append(f"{m} {'mês' if m == 1 else 'meses'}")
    return " e ".join(partes) if partes else "0 meses"


def formatar_chave(chave: str) -> str:
    """Traduz a chave técnica de um requisito/valor para um rótulo legível."""
    return TRADUCOES_CHAVES.get(chave, chave.replace("_", " ").capitalize())


def formatar_valor(valor):
    """Exibe floats inteiros sem casa decimal (5.0 -> 5)."""
    if isinstance(valor, float) and valor.is_integer():
        return int(valor)
    return valor
