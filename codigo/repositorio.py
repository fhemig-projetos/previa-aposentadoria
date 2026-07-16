import pandas as pd
from datetime import datetime
from codigo import Servidor


class RepositorioServidores:
    def __init__(self, caminho_excel: str):
#        self.caminho_excel = caminho_excel
#        self.df = pd.read_json(caminho_excel, dtype={"masp": str})
        self.caminho_excel = caminho_excel
        self.df = pd.read_excel(caminho_excel, dtype={"MASP": str})

    def buscar_por_masp(self, masp: str) -> Servidor | None:
        resultado = self.df[self.df["MASP"] == masp]

        if resultado.empty:
            return None

        dados = resultado.iloc[0]

        return Servidor(
            masp=dados["MASP"],
            nome=dados["Nome Servidor"],
            data_nascimento=dados["Data Completa"].date(),
            sexo=dados["Cod Sexo"],
            cargo=dados["Cod Carreira"],
            funcao=dados["Categoria Profissional/Ocupação"],
            data_admissao=dados["Data Exercício"].date()
        )