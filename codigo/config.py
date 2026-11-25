"""Caminhos e constantes compartilhadas do projeto.

Todos os caminhos são absolutos (calculados a partir deste arquivo), então o
sistema funciona independentemente da pasta de onde o comando é executado.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
DADOS_DIR = BASE_DIR / "dados"
OUTPUT_DIR = BASE_DIR / "output"

CAMINHO_EXCEL = DADOS_DIR / "dados_cadastrais.xlsx"
CAMINHO_JSON = DADOS_DIR / "dados_cadastrais.json"

LOGO_INTERFACE = ASSETS_DIR / "LogoFhemig.png"
ICONE_PAGINA = ASSETS_DIR / "icone.png"
LOGO_PDF = ASSETS_DIR / "cabecalho_pdf.png"

# Critério único de conversão de dias em anos (usado em modelos, projeção e regras).
DIAS_POR_ANO = 365.25
