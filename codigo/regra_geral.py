from datetime import date
from codigo import Servidor, DadosTempo, ResultadoRegra
from .regra_modelo import RegraAposentadoria
from .projecao import anos_de_dias, idade_em, projetar_data
import math

class RegraGeral(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="REGRA_GERAL", 
            nome="Regra Geral"
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
            idade_minima = 62
        else:
            idade_minima = 65     
        
        contribuicao_minima = 25        
        servico_publico_minimo = 10
        cargo_minimo = 5

        pendencias = []

        if servidor.idade < idade_minima:
            faltam = idade_minima - servidor.idade
            pendencias.append(
                f"{self._fmt_tempo(faltam)} de idade."
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
                "cargo_minimo": cargo_minimo
            },
            valores_apurados={
                "idade": servidor.idade,
                "anos_total_contribuicao": dados_tempo.anos_total_contribuicao,
                "anos_efetivo_exercicio": dados_tempo.anos_efetivo_exercicio,
                "anos_no_cargo": dados_tempo.anos_no_cargo,
            },
            pendencias=pendencias,
            observacoes=[
                "Base legal: Constituição Estadual de Minas Gerais de 1989, art. 36, alterado pela Emenda Constitucional nº 104 de 2020.",
            ],
            proventos=["Ao completar os requisitos mínimos os proventos serão de 100% da média (80% das maiores remunerações), reajustados conforme índice de atualização dos benefícios do RGPS."]
        )