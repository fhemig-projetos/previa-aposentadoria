from abc import ABC, abstractmethod
from codigo import Servidor, DadosTempo, ResultadoRegra
from datetime import date
from regra_modelo import RegraAposentadoria

class RegraPontos(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="REGRA_PONTOS",
            nome="Regra de Pontos"
        )

    def _meses_decorridos(self, inicio: date, fim: date) -> int:
        meses = (fim.year - inicio.year) * 12 + (fim.month - inicio.month)

        if fim.day < inicio.day:
            meses -= 1

        return max(0, meses)

    def _calcular_pontos_minimos(self, sexo: str, data_avaliacao: date) -> int:
        if sexo == "F":
            pontos_base = 86
            limite = 100
        else:
            pontos_base = 97
            limite = 105
        inicio_progressao = date(2021, 1, 1)

        if data_avaliacao < inicio_progressao:
            return pontos_base

        meses = self._meses_decorridos(inicio_progressao, data_avaliacao)

        acrescimo = 1 + (meses // 12)

        return min(pontos_base + acrescimo, limite)
    
    
    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        data_avaliacao = date.today()
        
        if servidor.sexo == "F":
            idade_minima = 55
            contribuicao_minima = 30
            #pontos_minimos = 86
        else:
            idade_minima = 61
            contribuicao_minima = 35
            #pontos_minimos = 96

        if data_avaliacao >= date(2022, 1, 1):
            if servidor.sexo == "F":
                idade_minima = 56
            else:
                idade_minima = 62

        pontos_minimos = self._calcular_pontos_minimos(
            servidor.sexo,
            data_avaliacao
        )    
        
        servico_publico_minimo = 10
        cargo_minimo = 5

        somatorio_pontos = servidor.idade + dados_tempo.anos_total_contribuicao

        cumpriu = (
            servidor.idade >= idade_minima
            and dados_tempo.anos_total_contribuicao >= contribuicao_minima
            and dados_tempo.anos_efetivo_exercicio >= servico_publico_minimo
            and dados_tempo.anos_no_cargo >= cargo_minimo
            and somatorio_pontos >= pontos_minimos
        )

        pendencias = []

        if servidor.idade < idade_minima:
            pendencias.append(
                f"Faltam {idade_minima - servidor.idade} anos de idade."
            )

        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            pendencias.append(
                f"Faltam {contribuicao_minima - dados_tempo.anos_total_contribuicao:.2f} anos de contribuição."
            )

        if dados_tempo.anos_efetivo_exercicio < servico_publico_minimo:
            pendencias.append(
                f"Faltam {servico_publico_minimo - dados_tempo.anos_efetivo_exercicio:.2f} anos de efetivo exercício no serviço público."
            )

        if dados_tempo.anos_no_cargo < cargo_minimo:
            pendencias.append(
                f"Faltam {cargo_minimo - dados_tempo.anos_no_cargo:.2f} anos no cargo."
            )

        if somatorio_pontos < pontos_minimos:
            pendencias.append(
                f"Faltam {pontos_minimos - somatorio_pontos:.2f} pontos."
            )
            return ResultadoRegra(
                codigo=self.codigo,
                nome=self.nome,
                cumpriu=cumpriu,
                valores_apurados={
                    "idade": servidor.idade,
                    "anos_total_contribuicao": dados_tempo.anos_total_contribuicao,
                    "anos_efetivo_exercicio": dados_tempo.anos_efetivo_exercicio,
                    "anos_no_cargo": dados_tempo.anos_no_cargo,
                    "somatorio_pontos": round(somatorio_pontos, 2),
                    "pontos_minimos": pontos_minimos,
                },
                requisitos={
                    "idade_minima": idade_minima,
                    "contribuicao_minima": contribuicao_minima,
                    "servico_publico_minimo": servico_publico_minimo,
                    "cargo_minimo": cargo_minimo,
                    "pontos_minimos": pontos_minimos,
                },
                pendencias=pendencias,
                observacoes=[
                    "Regra de pontos calculada conforme art. 146 da EC nº 104/2020.",
                    "A pontuação mínima é acrescida de 1 ponto a cada 1 ano e 3 meses a partir de 01/01/2021, limitada a 100 pontos para mulher e 105 pontos para homem."
                ]
            )

'''
Atenção a um detalhe jurídico-técnico

O § 3º diz que idade e tempo de contribuição serão apurados em dias para o cálculo do somatório de pontos. Então, o ideal é que servidor.idade e dados_tempo.anos_total_contribuicao não sejam apenas inteiros arredondados. O melhor seria usar algo como:

idade_em_anos = dias_de_idade / 365.25
tempo_contribuicao_em_anos = dias_contribuicao / 365.25
somatorio_pontos = idade_em_anos + tempo_contribuicao_em_anos

Se hoje servidor.idade estiver retornando só a idade inteira, sua calculadora pode negar uma regra que o servidor já cumpriu por fração de idade ou contribuição.
'''                