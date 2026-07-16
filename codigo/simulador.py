from codigo import Servidor, DadosTempo, ResultadoRegra
from codigo import (
    RegraAposentadoria,
    RegraIdadeTempoContribuicao,
    RegraDireitoAdquiridoEC41,
)


class SimuladorAposentadoria:
    def __init__(self):
        self.regras: list[RegraAposentadoria] = [
            RegraIdadeTempoContribuicao(),
            RegraDireitoAdquiridoEC41(),
        ]

    def simular(
        self,
        servidor: Servidor,
        dados_tempo: DadosTempo,
    ) -> list[ResultadoRegra]:
        resultados: list[ResultadoRegra] = []

        for regra in self.regras:
            resultado = regra.avaliar(servidor, dados_tempo)
            resultados.append(resultado)

        return resultados