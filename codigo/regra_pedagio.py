from codigo import Servidor, DadosTempo, ResultadoRegra
from datetime import date
from .regra_modelo import RegraAposentadoria
from .projecao import anos_de_dias, idade_em, projetar_data
import math

class RegraDireitoAdquirido(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="DA_EC104",
            nome="Regra Pedágio - Direito Adquirido na Emenda Constitucional nº 104 de 2020"
        )
        
    @staticmethod
    def _fmt_num(valor, casas: int = 1) -> str:
        """Mostra inteiro sem '.0' (5.0 -> '5') e decimal com vírgula (4.7 -> '4,7')."""
        valor = round(float(valor), casas)
        if valor.is_integer():
            return str(int(valor))
        return f"{valor:.{casas}f}".replace(".", ",")
    
    @staticmethod
    def _fmt_tempo(anos) -> str:
        """Converte anos decimais em 'X anos e Y meses'.
        5.0 -> '5 anos' | 4.6667 -> '4 anos e 8 meses' | 1.0833 -> '1 ano e 1 mês'
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

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        if servidor.sexo == "F":
            idade_minima = 55
            contribuicao_minima = 30
        else:
            idade_minima = 60
            contribuicao_minima = 35

        servico_publico_minimo = 20
        cargo_minimo = 5
        data_limite_ingresso = date(2003, 12, 31)

        pendencias = []
        #data limite ingresso somente limita os recebimentos de aposentadoria, não é requisito para aposentadoria
        #if servidor.data_admissao > data_limite_ingresso:
        #    pendencias.append(
        #        "Servidor ingressou no serviço público após 31/12/2003. "
        #        "Não atende ao requisito de ingresso máximo para direito adquirido."
        #    )
        if servidor.idade < idade_minima:
            pendencias.append(
                f"{self._fmt_tempo(idade_minima - servidor.idade)} de idade."
            )

        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            faltam = contribuicao_minima - dados_tempo.anos_total_contribuicao
            pendencias.append(
                f"{self._fmt_tempo(faltam)} de contribuição."
            )

        if dados_tempo.anos_efetivo_exercicio < servico_publico_minimo:
            faltam = servico_publico_minimo - dados_tempo.anos_efetivo_exercicio
            pendencias.append(
                f"{self._fmt_tempo(faltam)} de serviço público."
            )

        if dados_tempo.anos_no_cargo < cargo_minimo:
            faltam = cargo_minimo - dados_tempo.anos_no_cargo
            pendencias.append(
                f"{self._fmt_tempo(faltam)} no cargo."
            )

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
            proventos=
                ["Cálculo dos proventos I: Provento integral com base na última remuneração e com direito à paridade para o servidor que comprove cumulativamente o cumprimento de todos os requisitos para a aposentadoria e ingresso no cargo efetivo em que se dará a aposentadoria até 31/12/2003.",
                "Cálculo dos proventos II: Média aritmética de 80% das maiores remunerações de contribuições recebidas desde 07/1994. Achado o valor da média, aplica-se 100% do valor da média."]
            
        )