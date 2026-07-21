import pandas as pd
from datetime import datetime
from codigo import Servidor


class RepositorioServidores:
    def __init__(self, caminho_excel: str):
        self.caminho_excel = caminho_excel
        self.df = pd.read_json(caminho_excel, dtype={"masp": str})
        #self.df = pd.read_excel(caminho_excel, dtype={"MASP": str, "ADM": str})

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
