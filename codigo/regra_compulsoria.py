from codigo import Servidor, DadosTempo, ResultadoRegra
from .regra_modelo import RegraAposentadoria
from .projecao import idade_em, projetar_data
import math

class RegraCompulsoria(RegraAposentadoria):
    def __init__(self):
        super().__init__(
            codigo="REGRA_COMPULSORIA",
            nome="Regra de Aposentadoria Compulsória"
        )
    
    @staticmethod
    def _fmt_tempo(anos) -> str:
        """Converte anos decimais em 'X anos e Y meses'.
        5.0 -> '5 anos' | 4.6667 -> '4 anos e 8 meses' | 1.0833 -> '1 ano e 1 mês'
        """
        # round(..., 6) evita erro de ponto flutuante (ex.: 60.00000001 meses)
        total_meses = math.ceil(round(float(anos) * 12, 6))
        a, m = divmod(total_meses, 12)

        partes = []
        if a:
            partes.append(f"{a} {'ano' if a == 1 else 'anos'}")
        if m:
            partes.append(f"{m} {'mês' if m == 1 else 'meses'}")
        return " e ".join(partes) if partes else "0 meses"

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        idade_compulsoria = 75
        pendencias = []

        if servidor.idade < idade_compulsoria:
            faltam = idade_compulsoria - servidor.idade
            pendencias.append(
                f"{self._fmt_tempo(faltam)} para a aposentadoria compulsória."
            )

        cumpriu = len(pendencias) == 0

        data_previsao = None if cumpriu else projetar_data(
            lambda data: (
                idade_em(data, servidor.data_nascimento) >= idade_compulsoria
            )
        )

        return ResultadoRegra(
            codigo=self.codigo,
            nome=self.nome,
            cumpriu=cumpriu,
            data_previsao=data_previsao,
            requisitos={
                "idade_compulsoria": idade_compulsoria
            },
            valores_apurados={
                "idade": servidor.idade
            },
            pendencias=pendencias,
            observacoes=[
                "Base legal: Constituição Federal, Art. 40, §1º, III."
            ],
            proventos=["Média aritmética de 80% das maiores remunerações de contribuições recebidas desde 07/1994. Achado o valor da média, deve-se aplicar 60% aos 20 anos e mais 2% para cada ano que exceder o tempo mínimo de 20 anos, tanto para homem quanto para mulher. Caso o servidor comprove menos que 20 anos na data do aniversário de 75 anos, o tempo total de contribuição será utilizado proporcionalmente para a apuração do valor do provento."]
        )