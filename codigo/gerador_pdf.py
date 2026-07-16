from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os

from codigo import Servidor, ResultadoRegra


class PDFGenerator:
    def __init__(self, pasta_saida: str = "output"):
        self.pasta_saida = pasta_saida
        os.makedirs(self.pasta_saida, exist_ok=True)
        self.styles = getSampleStyleSheet()

    def gerar(
        self,
        servidor: Servidor,
        resultados: list[ResultadoRegra]
    ) -> str:
        caminho = os.path.join(
            self.pasta_saida,
            f"previa_aposentadoria_{servidor.masp}.pdf"
        )

        doc = SimpleDocTemplate(
            caminho,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        elementos = []

        self._adicionar_titulo(elementos)
        self._adicionar_dados_servidor(elementos, servidor)
        self._adicionar_resultados(elementos, resultados)
        self._adicionar_rodape(elementos)

        doc.build(elementos)

        return caminho

    def _adicionar_titulo(self, elementos: list):
        elementos.append(
            Paragraph("Prévia de Aposentadoria", self.styles["Title"])
        )
        elementos.append(Spacer(1, 20))

    def _adicionar_dados_servidor(
        self,
        elementos: list,
        servidor: Servidor
    ):
        elementos.append(
            Paragraph("Dados do servidor", self.styles["Heading2"])
        )

        dados_tabela = [
            ["MASP", servidor.masp],
            ["ADM", servidor.adm],
            ["Nome", servidor.nome],
            ["Data de Nascimento", servidor.data_nascimento.strftime("%d/%m/%Y")],
            ["Idade", f"{servidor.idade} anos"],
            ["Sexo", servidor.sexo],
            ["Cargo", servidor.cargo],
            ["Função", servidor.funcao],
            ["Data de admissão", servidor.data_admissao.strftime("%d/%m/%Y")]
        ]

        tabela = Table(dados_tabela, colWidths=[150, 330])
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        elementos.append(tabela)
        elementos.append(Spacer(1, 20))

    def _adicionar_resultados(
        self,
        elementos: list,
        resultados: list[ResultadoRegra]
    ):
        elementos.append(
            Paragraph("Resultado da simulação", self.styles["Heading2"])
        )

        for resultado in resultados:
            elementos.append(
                Paragraph(resultado.nome, self.styles["Heading3"])
            )

            status = "Cumprida" if resultado.cumpriu else "Não cumprida"

            elementos.append(
                Paragraph(f"<b>Status:</b> {status}", self.styles["BodyText"])
            )

            elementos.append(Spacer(1, 8))

            elementos.append(
                Paragraph("<b>Valores apurados:</b>", self.styles["BodyText"])
            )

            for chave, valor in resultado.valores_apurados.items():
                texto = f"{self._formatar_chave(chave)}: {valor}"
                elementos.append(Paragraph(texto, self.styles["BodyText"]))

            elementos.append(Spacer(1, 8))

            if resultado.pendencias:
                elementos.append(
                    Paragraph("<b>Pendências:</b>", self.styles["BodyText"])
                )

                for pendencia in resultado.pendencias:
                    elementos.append(
                        Paragraph(f"- {pendencia}", self.styles["BodyText"])
                    )
            else:
                elementos.append(
                    Paragraph(
                        "Não foram identificadas pendências para esta regra.",
                        self.styles["BodyText"]
                    )
                )

            if resultado.observacoes:
                elementos.append(Spacer(1, 8))
                elementos.append(
                    Paragraph("<b>Observações:</b>", self.styles["BodyText"])
                )

                for observacao in resultado.observacoes:
                    elementos.append(
                        Paragraph(f"- {observacao}", self.styles["BodyText"])
                    )

            elementos.append(Spacer(1, 18))

    def _adicionar_rodape(self, elementos: list):
        elementos.append(Spacer(1, 20))

        elementos.append(
            Paragraph(
                f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}.",
                self.styles["BodyText"]
            )
        )

        elementos.append(
            Paragraph(
                "Este documento possui caráter meramente informativo e não substitui análise oficial do órgão competente.",
                self.styles["Italic"]
            )
        )

    @staticmethod
    def _formatar_chave(chave: str) -> str:
        return chave.replace("_", " ").capitalize()