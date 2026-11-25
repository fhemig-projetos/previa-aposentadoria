"""Leitura da base cadastral (JSON) e busca de servidores."""

from pathlib import Path

import pandas as pd

from .modelos import Servidor

COLUNA_MASP_ADM = "Masp/Admissão"
COLUNAS_TEXTO = [COLUNA_MASP_ADM, "MASP", "Nº Admissão"]


class RepositorioServidores:
    def __init__(self, caminho_json: str | Path):
        self.caminho_json = caminho_json
        self.df = pd.read_json(
            self.caminho_json,
            dtype={
                "MASP": str,
                "Nº Admissão": str,
                COLUNA_MASP_ADM: str,
                "MASP/Admissão": str,
            },
        )
        self._normalizar_colunas()

    def _normalizar_colunas(self):
        for coluna in COLUNAS_TEXTO:
            if coluna in self.df.columns:
                self.df[coluna] = self.df[coluna].astype(str).str.strip()

    def buscar_por_masp_adm(self, masp: str, adm: str) -> Servidor | None:
        masp = masp.strip()
        adm = adm.strip()

        if COLUNA_MASP_ADM in self.df.columns:
            resultado = self.df[self.df[COLUNA_MASP_ADM] == f"{masp}{adm}"]
        else:
            # fallback: busca por MASP e ADM separadamente
            resultado = self.df[
                (self.df["MASP"] == masp) & (self.df["Nº Admissão"] == adm)
            ]

        if resultado.empty:
            return None

        dados = resultado.iloc[0]
        return Servidor(
            masp=dados["MASP"],
            adm=dados["Nº Admissão"],
            nome=dados["Nome Servidor"],
            data_nascimento=pd.to_datetime(dados["Data Completa"]).date(),
            sexo=dados["Cod Sexo"],
            cargo=dados["Cod Carreira"],
            funcao=dados["Categoria Profissional/Ocupação"],
            data_admissao=pd.to_datetime(dados["Data Exercício"]).date(),
        )
