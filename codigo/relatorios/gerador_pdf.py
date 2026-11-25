"""Geração do relatório em PDF da prévia de aposentadoria."""

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from ..config import LOGO_PDF, OUTPUT_DIR
from ..modelos import ResultadoRegra, Servidor
from ..utils.formatacao import formatar_chave

COR_PRINCIPAL = colors.HexColor("#108da5")
MARGEM = 40
ALTURA_CABECALHO = 90

# Relaciona cada requisito ao valor apurado correspondente (coluna da direita).
MAPA_REQUISITOS_VALORES = {
    "idade_minima": "idade",
    "contribuicao_minima": "anos_total_contribuicao",
    "servico_publico_minimo": "anos_efetivo_exercicio",
    "cargo_minimo": "anos_no_cargo",
    "ingresso_maximo": "data_admissao",
    "idade_compulsoria": "idade",
}


class PDFGenerator:
    def __init__(self, pasta_saida: str | Path = OUTPUT_DIR):
        self.pasta_saida = Path(pasta_saida)
        self.pasta_saida.mkdir(parents=True, exist_ok=True)

        self.styles = getSampleStyleSheet()
        self.estilo = ParagraphStyle(
            "Estilo",
            parent=self.styles["Heading2"],
            textColor=COR_PRINCIPAL,
            fontSize=15,
            leading=18,
            spaceAfter=5
        )

    def gerar(
        self,
        servidor: Servidor,
        resultados: list[ResultadoRegra]
    ) -> str:
        caminho = self.pasta_saida / f"previa_aposentadoria_{servidor.masp}.pdf"

        largura_pagina, altura_pagina = A4

        doc = BaseDocTemplate(
            str(caminho),
            pagesize=A4,
            rightMargin=MARGEM,
            leftMargin=MARGEM,
            topMargin=ALTURA_CABECALHO,
            bottomMargin=MARGEM
        )

        frame_primeira_pagina = Frame(
            x1=MARGEM,
            y1=MARGEM,
            width=largura_pagina - 2 * MARGEM,
            height=altura_pagina - ALTURA_CABECALHO - MARGEM,
            id="frame_primeira_pagina"
        )

        frame_demais_paginas = Frame(
            x1=MARGEM,
            y1=MARGEM,
            width=largura_pagina - 2 * MARGEM,
            height=altura_pagina - 2 * MARGEM,
            id="frame_demais_paginas"
        )

        template_primeira_pagina = PageTemplate(
            id="primeira_pagina",
            frames=[frame_primeira_pagina],
            onPage=self._adicionar_cabecalho,
            autoNextPageTemplate="demais_paginas"
        )

        template_demais_paginas = PageTemplate(
            id="demais_paginas",
            frames=[frame_demais_paginas]
        )

        doc.addPageTemplates([template_primeira_pagina, template_demais_paginas])

        elementos = []
        self._adicionar_dados_servidor(elementos, servidor)
        self._adicionar_resultados(elementos, resultados)
        self._adicionar_rodape(elementos)

        doc.build(elementos)
        return str(caminho)

    def _adicionar_cabecalho(self, canvas, doc):
        canvas.saveState()
        largura_pagina, altura_pagina = A4

        if LOGO_PDF.exists():
            canvas.drawImage(
                str(LOGO_PDF),
                x=MARGEM,
                y=altura_pagina - 85,
                width=largura_pagina - 2 * MARGEM,
                height=70,
                preserveAspectRatio=True,
            )

        canvas.restoreState()

    def _adicionar_dados_servidor(self, elementos: list, servidor: Servidor):
        elementos.append(Paragraph("Dados do Servidor", self.estilo))

        estilo_celula = ParagraphStyle(
            "CelulaTabela",
            parent=self.styles["BodyText"],
            fontSize=8,
            leading=12,
        )
        estilo_celula_titulo = ParagraphStyle(
            "CelulaTabelaTitulo",
            parent=estilo_celula,
            textColor=COR_PRINCIPAL,
        )

        campos = [
            ("MASP", str(servidor.masp)),
            ("Nº de Admissão", str(servidor.adm)),
            ("Nome", servidor.nome.title()),
            ("Data de Nascimento", servidor.data_nascimento.strftime("%d/%m/%Y")),
            ("Idade", f"{servidor.idade} anos"),
            ("Sexo", servidor.sexo),
            ("Cargo", servidor.cargo),
            ("Categoria Profissional", servidor.funcao.title()),
            ("Data de Admissão", servidor.data_admissao.strftime("%d/%m/%Y")),
        ]
        dados_tabela = [
            [
                Paragraph(f"<b>{rotulo}</b>", estilo_celula_titulo),
                Paragraph(valor, estilo_celula),
            ]
            for rotulo, valor in campos
        ]

        tabela = Table(dados_tabela, colWidths=[115, 200])
        tabela.hAlign = "LEFT"
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
            ("LINEAFTER", (0, 0), (0, -1), 0.75, COR_PRINCIPAL),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEADING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        elementos.append(tabela)
        elementos.append(Spacer(1, 20))

    @staticmethod
    def _lista_html(itens: list, vazio: str) -> str:
        if not itens:
            return vazio
        return "<br/>".join(f"- {item}" for item in itens)

    def _adicionar_resultados(
        self,
        elementos: list,
        resultados: list[ResultadoRegra]
    ):
        elementos.append(Paragraph("Resultado da Simulação", self.estilo))

        estilo_celula = ParagraphStyle(
            "CelulaResultado",
            parent=self.styles["BodyText"],
            fontSize=8,
            leading=12,
            alignment=TA_CENTER,
        )
        estilo_celula_cabecalho = ParagraphStyle(
            "CelulaResultadoCabecalho",
            parent=estilo_celula,
            textColor=colors.white,
            alignment=TA_CENTER,
        )

        largura_pagina, _ = A4
        corpo = self.styles["BodyText"]

        for resultado in resultados:
            elementos.append(Paragraph(resultado.nome, self.styles["Heading2"]))

            status = "Cumprida" if resultado.cumpriu else "Não cumprida"
            elementos.append(Paragraph(f"<b>Status:</b> {status}", corpo))
            elementos.append(Spacer(1, 6))

            pendencias = self._lista_html(
                resultado.pendencias, "Não foram identificadas pendências."
            )
            observacoes = self._lista_html(resultado.observacoes, "-")
            proventos = self._lista_html(resultado.proventos, "-")

            if resultado.data_previsao:
                data_prevista = resultado.data_previsao.strftime("%d/%m/%Y")
            elif resultado.cumpriu:
                data_prevista = "Requisitos já atendidos."
            else:
                data_prevista = (
                    "Não foi possível estimar a data de atendimento dos requisitos."
                )

            # Linhas da tabela: requisito | valor apurado
            linhas_tabela = []
            for chave_requisito, valor_requisito in resultado.requisitos.items():
                chave_valor = MAPA_REQUISITOS_VALORES.get(chave_requisito)
                if chave_valor and chave_valor in resultado.valores_apurados:
                    valor_apurado = resultado.valores_apurados[chave_valor]
                else:
                    valor_apurado = "-"

                celula_valor = (
                    f"<b>{formatar_chave(chave_valor)}:</b> {valor_apurado}"
                    if chave_valor else "-"
                )
                linhas_tabela.append([
                    Paragraph(
                        f"<b>{formatar_chave(chave_requisito)}:</b> {valor_requisito}",
                        estilo_celula
                    ),
                    Paragraph(celula_valor, estilo_celula),
                ])

            dados_tabela = [
                [
                    Paragraph("<b>Requisitos</b>", estilo_celula_cabecalho),
                    Paragraph("<b>Valores apurados</b>", estilo_celula_cabecalho),
                ],
                *linhas_tabela,
            ]

            tabela = Table(
                dados_tabela,
                colWidths=[(largura_pagina / 2) - MARGEM, (largura_pagina / 2) - MARGEM]
            )
            tabela.hAlign = "CENTER"
            tabela.setStyle(TableStyle([
                # (comando, (coluna_inicial, linha_inicial), (coluna_final, linha_final), valor)
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BACKGROUND", (0, 0), (-1, 0), COR_PRINCIPAL),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.white),
                ("LINEAFTER", (0, 0), (0, -1), 0.75, COR_PRINCIPAL),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]))

            elementos.append(tabela)
            elementos.append(Spacer(1, 6))

            for titulo, conteudo in (
                ("Pendência:", pendencias),
                ("Observações:", observacoes),
                ("Proventos:", proventos),
                ("Data prevista para atendimento dos requisitos:", data_prevista),
            ):
                elementos.append(Paragraph(f"<b>{titulo}</b>", corpo))
                elementos.append(Paragraph(conteudo, corpo))

    def _adicionar_rodape(self, elementos: list):
        elementos.append(Spacer(1, 6))
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
