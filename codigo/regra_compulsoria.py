from codigo import Servidor, DadosTempo, ResultadoRegra
from .regra_modelo import RegraAposentadoria

class RegraCompulsoria(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="REGRA_COMPULSORIA",
            nome="Regra de Aposentadoria Compulsória"
        )

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        idade_compulsoria = 75
        pendencias = []

        if servidor.idade < idade_compulsoria:
            faltam = idade_compulsoria - servidor.idade
            pendencias.append(
                f"Faltam {faltam} anos para a aposentadoria compulsória."
            )

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=len(pendencias) == 0,
            requisitos={
                "idade_compulsoria": idade_compulsoria
            },
            valores_apurados={
                "idade": servidor.idade
            },
            pendencias=pendencias,
            observacoes=[
                "Base legal: Constituição Federal, Art. 40, §1º, III."
            ]
        )

class RegraPontos(RegraAposentadoria):
    pass
'''    def __init__(self):
        super().__init__(
            codigo="REGRA_PONTOS",
            nome="Regra de Pontos"
        )
    
    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:'''