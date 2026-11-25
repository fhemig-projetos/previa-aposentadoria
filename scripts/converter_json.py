"""Converte a base Excel (dados/dados_cadastrais.xlsx) para JSON.

Uso (na raiz do projeto):
    python scripts/converter_json.py
    python scripts/converter_json.py --excel outro.xlsx --json saida.json --aba 0
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd  # noqa: E402

from codigo.config import CAMINHO_EXCEL, CAMINHO_JSON  # noqa: E402


def converter_excel_para_json(
    caminho_excel: str | Path,
    caminho_json: str | Path,
    nome_aba: str | int = 0,
):
    df = pd.read_excel(
        caminho_excel,
        sheet_name=nome_aba,
        engine="openpyxl"
    )
    df.to_json(
        caminho_json,
        orient="records",
        force_ascii=False,
        indent=4,
        date_format="iso"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--excel", default=str(CAMINHO_EXCEL))
    parser.add_argument("--json", default=str(CAMINHO_JSON))
    parser.add_argument("--aba", default=0, help="Nome ou índice da aba (padrão: 0)")
    args = parser.parse_args()

    aba = int(args.aba) if str(args.aba).isdigit() else args.aba
    converter_excel_para_json(args.excel, args.json, aba)
    print(f"Arquivo gerado: {args.json}")


if __name__ == "__main__":
    main()
