"""Núcleo do sistema de prévia de aposentadoria (sem dependência do Streamlit)."""

from .modelos import DadosTempo, ResultadoRegra, Servidor
from .regras import (
    RegraAposentadoria,
    RegraCompulsoria,
    RegraDireitoAdquirido,
    RegraGeral,
    RegraPontos,
)
from .relatorios import PDFGenerator
from .repositorio import RepositorioServidores
from .simulador import SimuladorAposentadoria

__all__ = [
    "Servidor",
    "DadosTempo",
    "ResultadoRegra",
    "RepositorioServidores",
    "RegraAposentadoria",
    "RegraDireitoAdquirido",
    "RegraCompulsoria",
    "RegraGeral",
    "RegraPontos",
    "SimuladorAposentadoria",
    "PDFGenerator",
]
