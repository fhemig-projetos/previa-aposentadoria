from .modelos import DadosTempo, ResultadoRegra, Servidor
from .regras import (
    RegraAposentadoria,
    RegraCompulsoria,
    RegraDireitoAdquirido,
    RegraGeral,
    RegraPontos,
)


class SimuladorAposentadoria:
    def __init__(self):
        self.regras: list[RegraAposentadoria] = [
            RegraDireitoAdquirido(),
            RegraGeral(),
            RegraCompulsoria(),
            RegraPontos(),
        ]

    def simular(
        self,
        servidor: Servidor,
        dados_tempo: DadosTempo,
    ) -> list[ResultadoRegra]:
        return [regra.avaliar(servidor, dados_tempo) for regra in self.regras]
