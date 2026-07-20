from abc import ABC, abstractmethod
from codigo import Servidor, DadosTempo, ResultadoRegra
from datetime import date


class RegraAposentadoria(ABC):
    def __init__(self, codigo: str, nome: str):
        self.codigo = codigo
        self.nome = nome

    @abstractmethod
    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        pass


class RegraIdadeTempoContribuicao(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="REGRA_IDADE_TEMPO",
            nome="Regra exemplo - idade e tempo de contribuição"
        )

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        if servidor.sexo == "F":
            idade_minima = 55
            contribuicao_minima = 30
        else:
            idade_minima = 60
            contribuicao_minima = 35

        tempo_minimo_cargo = 5

        pendencias = []

        if servidor.idade < idade_minima:
            faltam = idade_minima - servidor.idade
            pendencias.append(f"Faltam {faltam} anos de idade.")

        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            faltam = contribuicao_minima - dados_tempo.anos_total_contribuicao
            pendencias.append(
                f"Faltam aproximadamente {faltam:.2f} anos de contribuição."
            )

        if dados_tempo.anos_no_cargo < tempo_minimo_cargo:
            faltam = tempo_minimo_cargo - dados_tempo.anos_no_cargo
            pendencias.append(
                f"Faltam aproximadamente {faltam:.2f} anos no cargo."
            )

        cumpriu = len(pendencias) == 0

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=cumpriu,
            requisitos={
                "idade_minima": idade_minima,
                "contribuicao_minima": contribuicao_minima,
                "tempo_minimo_cargo": tempo_minimo_cargo
            },
            valores_apurados={
                "idade": servidor.idade,
                "anos_efetivo_exercicio": round(dados_tempo.anos_efetivo_exercicio, 2),
                "anos_contribuicao_externa": round(dados_tempo.anos_contribuicao_externa, 2),
                "anos_total_contribuicao": round(dados_tempo.anos_total_contribuicao, 2),
                "anos_no_cargo": round(dados_tempo.anos_no_cargo, 2),
                "anos_na_carreira": round(dados_tempo.anos_na_carreira, 2)
            },
            pendencias=pendencias,
            observacoes=[
                "Regra utilizada apenas como exemplo inicial.",
                "A simulação não substitui análise oficial do órgão competente."
            ]
        )
    
class RegraDireitoAdquiridoEC41(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="DA_EC41",
            nome="Direito adquirido - Art. 6º da EC 41/2003"
        )

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        if servidor.sexo == "F":
            idade_minima = 55
            contribuicao_minima = 30
        else:
            idade_minima = 60
            contribuicao_minima = 35

        servico_publico_minimo = 20
        carreira_minima = 10
        cargo_minimo = 5

        pendencias = []

        if servidor.idade < idade_minima:
            pendencias.append(
                f"Faltam {idade_minima - servidor.idade} anos de idade."
            )

        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            faltam = contribuicao_minima - dados_tempo.anos_total_contribuicao
            pendencias.append(
                f"Faltam aproximadamente {faltam:.2f} anos de contribuição."
            )

        if dados_tempo.anos_efetivo_exercicio < servico_publico_minimo:
            faltam = servico_publico_minimo - dados_tempo.anos_efetivo_exercicio
            pendencias.append(
                f"Faltam aproximadamente {faltam:.2f} anos de serviço público."
            )

        if dados_tempo.anos_na_carreira < carreira_minima:
            faltam = carreira_minima - dados_tempo.anos_na_carreira
            pendencias.append(
                f"Faltam aproximadamente {faltam:.2f} anos na carreira."
            )

        if dados_tempo.anos_no_cargo < cargo_minimo:
            faltam = cargo_minimo - dados_tempo.anos_no_cargo
            pendencias.append(
                f"Faltam aproximadamente {faltam:.2f} anos no cargo."
            )

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=len(pendencias) == 0,
            requisitos={
                "idade_minima": idade_minima,
                "contribuicao_minima": contribuicao_minima,
                "servico_publico_minimo": servico_publico_minimo,
                "carreira_minima": carreira_minima,
                "cargo_minimo": cargo_minimo
            },
            valores_apurados={
                "idade": servidor.idade,
                "anos_total_contribuicao": round(dados_tempo.anos_total_contribuicao, 2),
                "anos_efetivo_exercicio": round(dados_tempo.anos_efetivo_exercicio, 2),
                "anos_na_carreira": round(dados_tempo.anos_na_carreira, 2),
                "anos_no_cargo": round(dados_tempo.anos_no_cargo, 2)
            },
            pendencias=pendencias,
            observacoes=[
                "Previsão ilustrativa da regra.",
                "Necessária validação jurídica e previdenciária."
            ]
        )

class TetoINSS (RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="TETO_INSS",
            nome="Regra do Teto do INSS"
        )

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        pendencias = []

        if servidor.data_admissao >= date(2015, 2, 12) and not dados_tempo.sujeito_ao_teto_inss:
            pendencias.append(
                "Servidor admitido após 12/02/2015 deve estar sujeito ao teto do INSS."
            )

        cumpriu = len(pendencias) == 0

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=cumpriu,
            requisitos={
                "data_admissao": servidor.data_admissao.isoformat(),
                "sujeito_ao_teto_inss": dados_tempo.sujeito_ao_teto_inss
            },
            valores_apurados={
                "data_admissao": servidor.data_admissao.isoformat(),
                "sujeito_ao_teto_inss": dados_tempo.sujeito_ao_teto_inss
            },
            pendencias=pendencias,
            observacoes=[
                "Verificar se o servidor está sujeito ao teto do INSS conforme a data de admissão."
            ]
        )