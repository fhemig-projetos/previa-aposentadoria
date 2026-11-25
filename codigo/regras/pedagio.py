from datetime import date

from ..modelos import DadosTempo, ResultadoRegra, Servidor
from ..projecao import anos_de_dias, idade_em, projetar_data
from ..utils.formatacao import fmt_tempo
from .base import RegraAposentadoria


class RegraDireitoAdquirido(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="DA_EC104",
            nome="Regra Pedágio - Direito Adquirido na Emenda Constitucional nº 104 de 2020"
        )

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        if servidor.sexo == "F":
            idade_minima = 55
            contribuicao_minima = 30
        else:
            idade_minima = 60
            contribuicao_minima = 35

        servico_publico_minimo = 20
        cargo_minimo = 5

        pendencias = []

        # A data limite de ingresso (31/12/2003) somente limita a forma de
        # recebimento dos proventos; não é requisito para a aposentadoria e,
        # por isso, não gera pendência.

        if servidor.idade < idade_minima:
            pendencias.append(
                f"{fmt_tempo(idade_minima - servidor.idade)} de idade."
            )

        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            faltam = contribuicao_minima - dados_tempo.anos_total_contribuicao
            pendencias.append(f"{fmt_tempo(faltam)} de contribuição.")

        if dados_tempo.anos_efetivo_exercicio < servico_publico_minimo:
            faltam = servico_publico_minimo - dados_tempo.anos_efetivo_exercicio
            pendencias.append(f"{fmt_tempo(faltam)} de serviço público.")

        if dados_tempo.anos_no_cargo < cargo_minimo:
            faltam = cargo_minimo - dados_tempo.anos_no_cargo
            pendencias.append(f"{fmt_tempo(faltam)} no cargo.")

        cumpriu = len(pendencias) == 0
        hoje = date.today()

        def _atende_data(data: date) -> bool:
            dias_adicionais = max(0, (data - hoje).days)
            return (
                idade_em(data, servidor.data_nascimento) >= idade_minima
                and anos_de_dias(
                    dados_tempo.dias_total_contribuicao + dias_adicionais
                ) >= contribuicao_minima
                and anos_de_dias(
                    dados_tempo.dias_efetivo_exercicio + dias_adicionais
                ) >= servico_publico_minimo
                and anos_de_dias(
                    dados_tempo.dias_no_cargo + dias_adicionais
                ) >= cargo_minimo
            )

        data_previsao = None if cumpriu else projetar_data(_atende_data)

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=cumpriu,
            data_previsao=data_previsao,
            requisitos={
                "idade_minima": idade_minima,
                "contribuicao_minima": contribuicao_minima,
                "servico_publico_minimo": servico_publico_minimo,
                "cargo_minimo": cargo_minimo,
                "ingresso_maximo": "31/12/2003"
            },
            valores_apurados={
                "idade": servidor.idade,
                "anos_total_contribuicao": dados_tempo.anos_total_contribuicao,
                "anos_efetivo_exercicio": dados_tempo.anos_efetivo_exercicio,
                "anos_no_cargo": dados_tempo.anos_no_cargo,
                "data_admissao": servidor.data_admissao.strftime("%d/%m/%Y")
            },
            pendencias=pendencias,
            observacoes=[
                "Base Legal: Emenda Constitucional nº 104 de 2020.",
                "Reajuste dos Proventos: Os proventos serão reajustados na mesma data e índices em que se der o reajuste dos benefícios do RGPS."
            ],
            proventos=[
                "Cálculo dos proventos I: Provento integral com base na última remuneração e com direito à paridade para o servidor que comprove cumulativamente o cumprimento de todos os requisitos para a aposentadoria e ingresso no cargo efetivo em que se dará a aposentadoria até 31/12/2003.",
                "Cálculo dos proventos II: Média aritmética de 80% das maiores remunerações de contribuições recebidas desde 07/1994. Achado o valor da média, aplica-se 100% do valor da média."
            ]
        )
