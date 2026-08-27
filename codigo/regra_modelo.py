from abc import ABC, abstractmethod
from codigo import Servidor, DadosTempo, ResultadoRegra

class RegraAposentadoria(ABC):
    def __init__(self, codigo: str, nome: str):
        self.codigo = codigo
        self.nome = nome

    @abstractmethod
    def avaliar(self, servidor: Servidor, dados_tempo: DadosTempo) -> ResultadoRegra:
        pass




'''
REGRA GERAL:
Cálculo dos proventos: Média aritmética de 80% das maiores remunerações de contribuições recebidas desde 07/1994. Achado o valor da média, deve-se aplicar 60% aos 20 anos e mais 2% para cada ano que exceder o tempo mínimo de 20 anos, tanto para homem quanto para mulher.
Reajuste dos Proventos: Os proventos serão reajustados na mesma data e índices em que se der o reajuste dos benefícios do RGPS: Art. 7º, §7º da L.C. nº 64/2002, redação dada pela L.C. nº 156/2020.


TRANSIÇÃO DE PONTOS:
Cálculo dos proventos I: Provento integral com base na última remuneração e com direito a paridade, Art. 146, §6º, inciso I e §7º, inciso I, do ADCT, acrescentado pela E.C. nº 104/2020, desde que comprove cumulativamente: a) Cumprimento de todos os requisitos para a aposentadoria; b) Ingresso no cargo efetivo em que se dará a aposentadoria até 31/12/2003. c) 60 anos de idade, se mulher; 65 anos de idade, se homem.
Cálculo dos proventos II: Média aritmética de 80% das maiores remunerações de contribuições recebidas desde 07/1994. Achado o valor da média, aplica-se 100% do valor da média.
Reajuste dos Proventos: Os proventos serão reajustados na mesma data e índices em que se der o reajuste dos benefícios do RGPS: Art. 146, §7º, inciso II, do ADCT, acrescentado pela E.C. nº 104/2020.
Para o servidor que tenha ingressado no serviço público até 16/12/1998, sem interrupção, a idade mínima exigida será reduzida em um dia de idade para cada dia de contribuição que exceder o tempo de contribuição exigido: Art. 146, §10 da E.C. nº 104/2020. 
"	

TRANSIÇÃO POR PEDÁGIO:
"Período adicional de contribuição: Correspondente a 50% do tempo que, em 15/09/2020 (data da E.C. nº 104/2020), faltaria para atingir o tempo mínimo exigido de 35 anos para homem; 30 anos para mulher.
Cálculo dos proventos I: Provento integral com base na última remuneração e com direito à paridade: Art. 147, §2º, inciso I, e §3º, inciso I, do ADCT, acrescentado pela E.C. nº 104/2020 para o servidor que comprove cumulativamente: a) Cumprimento de todos os requisitos para a aposentadoria e b) Ingresso no cargo efetivo em que se dará a aposentadoria até 31/12/2003. 
Cálculo dos proventos II: Média aritmética de 80% das maiores remunerações de contribuições recebidas desde 07/1994. Achado o valor da média, aplica-se 100% do valor da média: Art. 147, §2º, inciso II, e §3º, inciso II, do ADCT, acrescentado pela E.C. nº 104/2020 (média sem paridade).
Reajuste dos Proventos: Os proventos serão reajustados na mesma data e índices em que se der o reajuste dos benefícios do RGPS.
Para o servidor que tenha ingressado no serviço público até 16/12/1998, sem interrupção, a idade mínima exigida será reduzida em um dia de idade para cada dia de contribuição que exceder o tempo de contribuição exigido: Art. 147, §5º da E.C. nº 104/2020."			

'''