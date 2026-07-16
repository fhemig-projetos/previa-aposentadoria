import pandas as pd

def converter_excel_para_json(
    caminho_excel: str,
    caminho_json: str,
    nome_aba: str | int = 0
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

    print(f"Arquivo JSON gerado com sucesso: {caminho_json}")


if __name__ == "__main__":
    converter_excel_para_json(
        caminho_excel="dados_cadastrais.xlsx",
        caminho_json="dados_cadastrais.json"
    )
