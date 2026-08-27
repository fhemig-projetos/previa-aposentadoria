from datetime import date

from codigo import Servidor, DadosTempo, ResultadoRegra
from .regra_modelo import RegraAposentadoria


class RegraPontos(RegraAposentadoria):
    """Regra da transição por pontuação — art. 146 da EC nº 104/2020.

    - Pontuação mínima: a partir de 01/01/2021 é acrescida de 1 ponto a cada
      um ano e três meses, até o limite de 100 pontos (mulher) e 105 (homem).
    - Cálculo dos proventos I (integral com direito à paridade) para quem
      cumprir, cumulativamente, todos os requisitos da regra, tiver ingressado
      no cargo efetivo até 31/12/2003 e atingir 60 anos (mulher) ou 65 (homem).
    - Cálculo dos proventos II: média aritmética de 80% das maiores
      remunerações desde 07/1994, aplicando-se 100% do valor médio.
    - Art. 146, §10: a idade mínima exigida é reduzida em 1 dia para cada dia
      de contribuição que exceder o tempo mínimo, para quem ingressou no
      serviço público até 16/12/1998, sem interrupção.
    """

    INICIO_PROGRESSAO = date(2021, 1, 1)
    INGRESSO_REDUCAO = date(1998, 12, 16)
    DIAS_POR_ANO = 365.25

    def __init__(self):
        super().__init__(
            codigo="REGRA_PONTOS",
            nome="Regra de Pontos"
        )

    def _meses_decorridos(self, inicio: date, fim: date) -> int:
        meses = (fim.year - inicio.year) * 12 + (fim.month - inicio.month)
        if fim.day < inicio.day:
            meses -= 1
        return max(0, meses)

    def _calcular_pontos_minimos(self, sexo: str, data_avaliacao: date) -> int:
        if sexo == "F":
            pontos_base, limite = 86, 100
        else:
            pontos_base, limite = 97, 105

        if data_avaliacao < self.INICIO_PROGRESSAO:
            return pontos_base

        meses = self._meses_decorridos(self.INICIO_PROGRESSAO, data_avaliacao)

        # A partir de 01/01/2021: +1 ponto a cada 1 ano e 3 meses (15 meses)
        acrescimo = meses // 15
        return min(pontos_base + acrescimo, limite)

    def _dias_total_contribuicao(self, dados_tempo: DadosTempo) -> int:
        """Total em dias das contribuições que compõem o tempo de contribuição
        (mesma base da propriedade anos_total_contribuicao)."""
        return (dados_tempo.dias_efetivo_exercicio
                + dados_tempo.dias_contribuicao_externa)

    def _calcular_reducao_idade_minima(
        self,
        servidor: Servidor,
        dados_tempo: DadosTempo,
        contribuicao_minima: int,
    ) -> int:
        """Art. 146, §10 da EC nº 104/2020.

        Quem ingressou no serviço público até 16/12/1998, sem interrupção,
        tem a idade mínima reduzida em um dia de idade para cada dia de
        contribuição que exceder o tempo mínimo exigido.
        """
        if servidor.data_admissao is None:
            return 0
        if servidor.data_admissao > self.INGRESSO_REDUCAO:
            return 0
        if not dados_tempo.interrupcao:
            return 0

        dias_exigidos = int(contribuicao_minima * self.DIAS_POR_ANO)
        dias_totais = self._dias_total_contribuicao(dados_tempo)
        return max(0, dias_totais - dias_exigidos)

    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        data_avaliacao = date.today()

        if servidor.sexo == "F":
            contribuicao_minima = 30
        else:
            contribuicao_minima = 35

        servico_publico_minimo = 10
        cargo_minimo = 5

        pontos_minimos = self._calcular_pontos_minimos(
            servidor.sexo,
            data_avaliacao,
        )

        # A idade mínima da regra de pontos corresponde à pontuação mínima
        # menos o tempo mínimo de contribuição (ex.: mulher em 2021:
        # 86 pontos - 30 anos = 56 anos).
        idade_minima = pontos_minimos - contribuicao_minima

        # Art. 146, §10: idade mínima reduzida em 1 dia para cada dia de
        # contribuição que exceder o tempo mínimo exigido (ingresso no serviço
        # público até 16/12/1998, sem interrupção).
        reducao_dias = self._calcular_reducao_idade_minima(
            servidor,
            dados_tempo,
            contribuicao_minima,
        )
        idade_minima_efetiva = idade_minima - (reducao_dias / self.DIAS_POR_ANO)

        somatorio_pontos = servidor.idade + dados_tempo.anos_total_contribuicao

        pendencias = []

        if servidor.idade < idade_minima_efetiva:
            faltam = idade_minima_efetiva - servidor.idade
            pendencias.append(f"Faltam {faltam:.2f} anos de idade.")

        if dados_tempo.anos_total_contribuicao < contribuicao_minima:
            faltam = contribuicao_minima - dados_tempo.anos_total_contribuicao
            pendencias.append(f"Faltam {faltam} anos de contribuição.")

        if dados_tempo.anos_efetivo_exercicio < servico_publico_minimo:
            faltam = servico_publico_minimo - dados_tempo.anos_efetivo_exercicio
            pendencias.append(f"Faltam {faltam} anos de serviço público.")

        if dados_tempo.anos_no_cargo < cargo_minimo:
            faltam = cargo_minimo - dados_tempo.anos_no_cargo
            pendencias.append(f"Faltam {faltam} anos no cargo.")

        if somatorio_pontos < pontos_minimos:
            faltam = pontos_minimos - somatorio_pontos
            pendencias.append(f"Faltam {faltam} pontos.")

        observacoes = [
            "Base legal: Constituição Estadual de Minas Gerais de 1989, art. 36, "
            "alterado pela Emenda Constitucional nº 104 de 2020, art. 146 do ADCT.",
            "Reajuste dos Proventos: Os proventos serão reajustados na mesma data e "
            "índices em que se der o reajuste dos benefícios do RGPS: Art. 146, §7º, "
            "inciso II, do ADCT, acrescentado pela E.C. nº 104/2020.",
        ]
        if reducao_dias > 0:
            observacoes.append(
                f"Art. 146, §10 da E.C. nº 104/2020: idade mínima reduzida em "
                f"{reducao_dias} dia(s), por contribuição excedente ao tempo mínimo, "
                f"em razão de ingresso no serviço público até 16/12/1998, sem "
                f"interrupção."
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
                "pontos_minimos": pontos_minimos,
            },
            valores_apurados={
                "idade": servidor.idade,
                "anos_total_contribuicao": dados_tempo.anos_total_contribuicao,
                "anos_efetivo_exercicio": dados_tempo.anos_efetivo_exercicio,
                "anos_no_cargo": dados_tempo.anos_no_cargo,
                "somatorio_pontos": somatorio_pontos,
                "pontos_minimos": pontos_minimos,
                "idade_minima_efetiva": round(idade_minima_efetiva, 2),
            },
            pendencias=pendencias,
            observacoes=observacoes,
            proventos=(
                "Média aritmética de 80% das maiores remunerações de contribuições "
                "recebidas desde 07/1994. Achado o valor da média, aplica-se 100% do "
                "valor da média: Art. 146, §7º, inciso II, do ADCT, acrescentado pela "
                "E.C. nº 104/2020. Para quem cumprir, cumulativamente, todos os "
                "requisitos da regra, tiver ingressado no cargo efetivo em que se dará "
                "a aposentadoria até 31/12/2003 e atingir 60 anos (mulher) ou 65 anos "
                "(homem): provento integral com base na última remuneração e com "
                "direito à paridade: Art. 146, §6º, inciso I e §7º, inciso I, do ADCT, "
                "acrescentado pela E.C. nº 104/2020."
            ),
        )
