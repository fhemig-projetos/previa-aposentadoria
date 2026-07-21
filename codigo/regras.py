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

class RegraDireitoAdquirido(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="DA_EC104",
            nome="Regra Pedágio - Direito Adquirido na Emenda Constitucional nº 104 de 2020"
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
        data_limite_ingresso = date(2003, 12, 31)
        #data_limite_requisitos = date(2020,9,15)

        pendencias = []
        
        if servidor.data_admissao > data_limite_ingresso:
            pendencias.append(
                "Servidor ingressou no serviço público após 31/12/2003. "
                "Não atende ao requisito de ingresso máximo para direito adquirido."
            )
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
# ENTENDER MELHOR CONTRIBUIÇÃO NA CARREIRA = 10 ANOS
# DIFERENÇA ENTRE CARREIRA E CARGO?
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
                "cargo_minimo": cargo_minimo,
                "ingresso_maximo": "31/12/2003"
            },
            valores_apurados={
                "idade": servidor.idade,
                "anos_total_contribuicao": round(dados_tempo.anos_total_contribuicao, 2),
                "anos_efetivo_exercicio": round(dados_tempo.anos_efetivo_exercicio, 2),
                "anos_na_carreira": round(dados_tempo.anos_na_carreira, 2),
                "anos_no_cargo": round(dados_tempo.anos_no_cargo, 2),
                "data_admissao": servidor.data_admissao.strftime("%d/%m/%Y")
            },
            pendencias=pendencias,
            observacoes=[
                "Previsão ilustrativa da regra.",
                "Necessária validação jurídica e previdenciária."
            ]
        )
    
class RegraGeral(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="REGRA_GERAL", 
            nome="Regra Geral"
        )

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        if servidor.sexo == "F":
            idade_minima = 62
        else:
            idade_minima = 65     
        
        contribuicao_minima = 25        
        tempo_minimo_servico_publico = 10
        tempo_minimo_cargo = 5

        pendencias = []

        if servidor.idade < idade_minima:
            faltam = idade_minima - servidor.idade
            pendencias.append(
                f"Faltam {faltam:.2f} anos de idade."
            )
        
        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            faltam = contribuicao_minima - dados_tempo.anos_total_contribuicao
            pendencias.append(
                f"Faltam {faltam:.2f} anos de contribuição."
            )
        
        if dados_tempo.anos_efetivo_exercicio < tempo_minimo_servico_publico:
            faltam = tempo_minimo_servico_publico - dados_tempo.anos_efetivo_exercicio
            pendencias.append(
                f"Faltam {faltam:.2f} anos de serviço público."
            )
        
        if dados_tempo.anos_no_cargo < tempo_minimo_cargo:
            faltam = tempo_minimo_cargo < dados_tempo.anos_no_cargo
            pendencias.append(
                f"Faltam {faltam:.2f} anos no cargo."
            )
        
        cumpriu = len(pendencias) == 0

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=cumpriu,
            requisitos={
                "idade_minima": idade_minima,
                "contribuicao_minima": contribuicao_minima,
                "tempo_minimo_servico_publico": tempo_minimo_servico_publico,
                "tempo_minimo_cargo": tempo_minimo_cargo
            },
            valores_apurados={
                "idade": servidor.idade,
                "anos_total_contribuicao": round(dados_tempo.anos_total_contribuicao,2),
                "anos_efetivo_exercicio": round(dados_tempo.anos_efetivo_exercicio,2),
                "anos_no_cargo": round(dados_tempo.anos_no_cargo,2)
            },
            pendencias=pendencias,
            observacoes=[
                "Previsão ilustrativa da regra.",
                "Para se aposentar pelas regras permanentes, é necessário que o servidor cumpra cumulativamente todas as exigências.",
            ]
        )

class RegraPontos(RegraAposentadoria):
    pass
'''    def __init__(self):
        super().__init__(
            codigo="REGRA_PONTOS",
            nome="Regra de Pontos"
        )
    
    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:'''