from abc import ABC, abstractmethod
from codigo import Servidor, DadosTempo, ResultadoRegra

class RegraAposentadoria(ABC):
    def __init__(self, codigo: str, nome: str):
        self.codigo = codigo
        self.nome = nome

    @abstractmethod
    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        pass