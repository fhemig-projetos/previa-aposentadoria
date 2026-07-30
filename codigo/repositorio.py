from pathlib import Path

import pandas as pd

from codigo import Servidor


class RepositorioServidores:
    def __init__(self, caminho_dados: str | Path):
        self.caminho_dados = Path(caminho_dados)
        self.df = self._carregar_dataframe()

    def _carregar_dataframe(self) -> pd.DataFrame:
        if not self.caminho_dados.exists():
            raise FileNotFoundError(
                f"Arquivo de dados não encontrado: {self.caminho_dados}"
            )

        extensao = self.caminho_dados.suffix.lower()

        if extensao == ".json":
            return pd.read_json(self.caminho_dados, dtype={"MASP": str})

        if extensao == ".xlsx":
            return pd.read_excel(
                self.caminho_dados,
                sheet_name=0,
                engine="openpyxl",
                dtype={"MASP": str, "ADM": str},
            )

        raise ValueError(f"Formato não suportado: {self.caminho_dados}")

    def buscar_por_masp_adm(self, masp: str, adm: str) -> Servidor | None:
        masp_adm_busca = f"{masp}{adm}"
        coluna_busca = "Masp/Admissão"

        if coluna_busca in self.df.columns:
            self.df[coluna_busca] = self.df[coluna_busca].astype(str)
            resultado = self.df[self.df[coluna_busca] == masp_adm_busca]
        else:
            # fallback: busca por MASP e ADM separadamente
            resultado = self.df[
                (self.df["MASP"] == masp) & (self.df["ADM"] == adm)
            ]

        if resultado.empty:
            return None

        dados = resultado.iloc[0]

        return Servidor(
            masp=dados["MASP"],
            adm=dados["Nº Admissão"],
            nome=dados["Nome Servidor"],
            data_nascimento= pd.to_datetime(dados["Data Completa"]).date(),
            sexo=dados["Cod Sexo"],
            cargo=dados["Cod Carreira"],
            funcao=dados["Categoria Profissional/Ocupação"],
            data_admissao=pd.to_datetime(dados["Data Exercício"]).date()
        )
