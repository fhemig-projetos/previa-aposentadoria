from dataclasses import dataclass
from datetime import date
from dateutil.relativedelta import relativedelta


@dataclass
class Servidor:
    masp: str
    adm: str
    nome: str
    data_nascimento: date
    sexo: str
    cargo: str
    funcao: str
    data_admissao: date
    sujeito_ao_teto_inss: bool | None = None
    dias_sem_interrupcao: bool | None = None
    
    @property
    def masp_adm(self) -> str:
        return f"{self.masp}{self.adm}"
    
    @property
    def idade(self) -> int:
        hoje = date.today()
        return relativedelta(hoje, self.data_nascimento).years


@dataclass
class DadosTempo:
    dias_efetivo_exercicio: int
    dias_contribuicao_externa: int
    dias_no_cargo: int
    dias_na_carreira: int
    sujeito_ao_teto_inss: bool = False

    @staticmethod
    def dias_para_anos(dias: int) -> float:
        return dias / 365.25

    @property
    def anos_efetivo_exercicio(self) -> float:
        return self.dias_para_anos(self.dias_efetivo_exercicio)

    @property
    def anos_contribuicao_externa(self) -> float:
        return self.dias_para_anos(self.dias_contribuicao_externa)

    @property
    def anos_total_contribuicao(self) -> float:
        return self.anos_efetivo_exercicio + self.anos_contribuicao_externa

    @property
    def anos_no_cargo(self) -> float:
        return self.dias_para_anos(self.dias_no_cargo)

    @property
    def anos_na_carreira(self) -> float:
        return self.dias_para_anos(self.dias_na_carreira)


@dataclass
class ResultadoRegra:
    codigo: str
    nome: str
    cumpriu: bool
    requisitos: dict
    valores_apurados: dict
    pendencias: list
    observacoes: list