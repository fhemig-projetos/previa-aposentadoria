"""Classe base das regras de aposentadoria.

O texto legal de cada regra (cálculo dos proventos, reajuste etc.) está em
``docs/regras_legais.md``.
"""

from abc import ABC, abstractmethod

from ..modelos import DadosTempo, ResultadoRegra, Servidor


class RegraAposentadoria(ABC):
    def __init__(self, codigo: str, nome: str):
        self.codigo = codigo
        self.nome = nome

    @abstractmethod
    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        pass
