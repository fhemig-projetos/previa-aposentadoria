from codigo import Servidor, DadosTempo, ResultadoRegra
from .regra_modelo import RegraAposentadoria

class RegraGeral(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="REGRA_GERAL", 
            nome="Regra Geral"
        )

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
                f"Faltam {faltam} anos de idade."
            )
        
        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            faltam = contribuicao_minima - dados_tempo.anos_total_contribuicao
            pendencias.append(
                f"Faltam {faltam} anos de contribuição."
            )
        
        if dados_tempo.anos_efetivo_exercicio < servico_publico_minimo:
            faltam = servico_publico_minimo - dados_tempo.anos_efetivo_exercicio
            pendencias.append(
                f"Faltam {faltam} anos de serviço público."
            )
        
        if dados_tempo.anos_no_cargo < cargo_minimo:
            faltam = cargo_minimo - dados_tempo.anos_no_cargo
            pendencias.append(
                f"Faltam {faltam} anos no cargo."
            )
        
        cumpriu = len(pendencias) == 0

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=cumpriu,
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
            ]
        )