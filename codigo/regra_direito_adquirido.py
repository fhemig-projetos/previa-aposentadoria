from codigo import Servidor, DadosTempo, ResultadoRegra
from datetime import date
from regra_modelo import RegraAposentadoria

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
        cargo_minimo = 5
        data_limite_ingresso = date(2003, 12, 31)

        pendencias = []
        #data limite ingresso somente limita os recebimentos de aposentadoria, não é requisito para aposentadoria
        #if servidor.data_admissao > data_limite_ingresso:
        #    pendencias.append(
        #        "Servidor ingressou no serviço público após 31/12/2003. "
        #        "Não atende ao requisito de ingresso máximo para direito adquirido."
        #    )
        if servidor.idade < idade_minima:
            pendencias.append(
                f"Faltam {idade_minima - servidor.idade} anos de idade."
            )

        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            faltam = contribuicao_minima - dados_tempo.anos_total_contribuicao
            pendencias.append(
                f"Faltam {faltam} anos de contribuição."
            )

        if dados_tempo.anos_efetivo_exercicio < servico_publico_minimo:
            faltam = servico_publico_minimo - dados_tempo.anos_efetivo_exercicio
            pendencias.append(
                f"Faltam {faltam} anos de serviço público."
            )

        if dados_tempo.anos_no_cargo < cargo_minimo:
            faltam = cargo_minimo - dados_tempo.anos_no_cargo
            pendencias.append(
                f"Faltam  {faltam} anos no cargo."
            )

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=len(pendencias) == 0,
            requisitos={
                "idade_minima": idade_minima,
                "contribuicao_minima": contribuicao_minima,
                "servico_publico_minimo": servico_publico_minimo,
                "cargo_minimo": cargo_minimo,
                "ingresso_maximo": "31/12/2003"
            },
            valores_apurados={
                "idade": servidor.idade,
                "anos_total_contribuicao": dados_tempo.anos_total_contribuicao,
                "anos_efetivo_exercicio": dados_tempo.anos_efetivo_exercicio,
                "anos_no_cargo": dados_tempo.anos_no_cargo,
                "data_admissao": servidor.data_admissao.strftime("%d/%m/%Y")
            },
            pendencias=pendencias,
            observacoes=[
                "Base Legal: Emenda Constitucional nº 104 de 2020."
            ]
        )