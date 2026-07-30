import pandas as pd
from codigo import Servidor


class RepositorioServidores:
    def __init__(self, caminho_json: str):
        self.caminho_json = caminho_json

        self.df = pd.read_json(
            self.caminho_json,
            dtype={
                "MASP": str,
                "ADM": str,
                "Nº Admissão": str,
                "Masp/Admissão": str,
            }
        )

        self._normalizar_colunas()

    def _normalizar_colunas(self):
        """
        Garante que as colunas usadas na busca estejam em formato texto.
        Isso evita problemas quando MASP, ADM ou Nº Admissão vêm como número.
        """

        colunas_texto = [
            "MASP",
            "ADM",
            "Nº Admissão",
            "Masp/Admissão",
        ]

        for coluna in colunas_texto:
            if coluna in self.df.columns:
                self.df[coluna] = self.df[coluna].astype(str).str.strip()

    def buscar_por_masp_adm(self, masp: str, adm: str) -> Servidor | None:
        masp = str(masp).strip()
        adm = str(adm).strip()

        masp_adm_busca = f"{masp}{adm}"

        if "Masp/Admissão" in self.df.columns:
            resultado = self.df[
                self.df["Masp/Admissão"] == masp_adm_busca
            ]

        elif "MASP" in self.df.columns and "Nº Admissão" in self.df.columns:
            resultado = self.df[
                (self.df["MASP"] == masp) &
                (self.df["Nº Admissão"] == adm)
            ]

        elif "MASP" in self.df.columns and "ADM" in self.df.columns:
            resultado = self.df[
                (self.df["MASP"] == masp) &
                (self.df["ADM"] == adm)
            ]

        else:
            raise ValueError(
                "O JSON não possui colunas suficientes para buscar por MASP e admissão."
            )

        if resultado.empty:
            return None

        dados = resultado.iloc[0]

        return Servidor(
            masp=str(dados["MASP"]),
            adm=str(dados["Nº Admissão"]),
            nome=dados["Nome Servidor"],
            data_nascimento=pd.to_datetime(dados["Data Completa"]).date(),
            sexo=dados["Cod Sexo"],
            cargo=dados["Cod Carreira"],
            funcao=dados["Categoria Profissional/Ocupação"],
            data_admissao=pd.to_datetime(dados["Data Exercício"]).date()
        )