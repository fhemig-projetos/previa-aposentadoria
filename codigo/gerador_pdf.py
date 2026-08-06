from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import NextPageTemplate, PageBreak
from pathlib import Path
from datetime import datetime
import os

from codigo import Servidor, ResultadoRegra

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "assets" / "cabecalho_pdf.png"

class PDFGenerator:
    def __init__(self, pasta_saida: str = "output"):
        self.pasta_saida = pasta_saida
        os.makedirs(self.pasta_saida, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self.estilo = ParagraphStyle(
            "Estilo",
            parent=self.styles["Heading2"],
            textColor=colors.HexColor("#108da5"),
            fontSize=15,
            leading=18,
            spaceAfter=5
        )

    def gerar(
        self,
        servidor: Servidor,
        resultados: list[ResultadoRegra]
    ) -> str:
        caminho = os.path.join(
            self.pasta_saida,
            f"previa_aposentadoria_{servidor.masp}.pdf"
        )

        largura_pagina, altura_pagina = A4

        doc = BaseDocTemplate(
            caminho,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=90,
            bottomMargin=40
        )

        frame_primeira_pagina = Frame(
            x1=40,
            y1=40,
            width=largura_pagina - 80,
            height=altura_pagina - 90 - 40,
            id="frame_primeira_pagina"
        )

        frame_demais_paginas = Frame(
            x1=40,
            y1=40,
            width=largura_pagina - 80,
            height=altura_pagina - 40 - 40,
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

        doc.addPageTemplates(
            [
            template_primeira_pagina,
            template_demais_paginas
            ]
        )

        elementos = []

        self._adicionar_dados_servidor(elementos, servidor)
        self._adicionar_resultados(elementos, resultados)
        self._adicionar_rodape(elementos)

        doc.build(elementos)

        return caminho

    def _adicionar_cabecalho(self, canvas, doc):
        canvas.saveState()
        largura_pagina, altura_pagina = A4

        if LOGO_PATH.exists():            
            canvas.drawImage(
                str(LOGO_PATH),
                x=40,
                y=altura_pagina- 85,
                width=largura_pagina - 80,
                height=70,
                preserveAspectRatio=True,
            )

        canvas.restoreState()

    #def _pagina_sem_cabecalho(self, canvas, doc):
    #    pass
    def _configurar_pagina(self, canvas, doc):
        if doc.page == 1:
            self._adicionar_cabecalho(canvas, doc)
        

    def _adicionar_dados_servidor(
        self,
        elementos: list,
        servidor: Servidor
    ):
        elementos.append(
            Paragraph(
                "Dados do Servidor", 
                self.estilo
            )
        )

        estilo_celula = ParagraphStyle(
            "CelulaTabela",
            parent=self.styles["BodyText"],
            fontSize=8,
            leading=12,
        )
        estilo_celula_titulo = ParagraphStyle(
            "CelulaTabelaTitulo",
            parent=estilo_celula,
            #fontName="Helvetica-Bold",
            textColor=colors.HexColor("#108da5"),
        )

        dados_tabela = [
            [
                Paragraph("<b>MASP</b>", estilo_celula_titulo),
                Paragraph(str(servidor.masp), estilo_celula),
            ],
            [
                Paragraph("<b>Nº de Admissão</b>", estilo_celula_titulo),
                Paragraph(str(servidor.adm), estilo_celula),
            ],
            [
                Paragraph("<b>Nome</b>", estilo_celula_titulo),
                Paragraph(servidor.nome.title(), estilo_celula),
            ],
            [
                Paragraph("<b>Data de Nascimento</b>", estilo_celula_titulo),
                Paragraph(servidor.data_nascimento.strftime("%d/%m/%Y"), estilo_celula),
            ],
            [
                Paragraph("<b>Idade</b>", estilo_celula_titulo),
                Paragraph(f"{servidor.idade} anos", estilo_celula),
            ],
            [
                Paragraph("<b>Sexo</b>", estilo_celula_titulo),
                Paragraph(servidor.sexo, estilo_celula),
            ],
            [
                Paragraph("<b>Cargo</b>", estilo_celula_titulo),
                Paragraph(servidor.cargo, estilo_celula),
            ],
            [
                Paragraph("<b>Categoria Profissional</b>", estilo_celula_titulo),
                Paragraph(servidor.funcao.title(), estilo_celula),
            ],
            [
                Paragraph("<b>Data de Admissão</b>", estilo_celula_titulo),
                Paragraph(servidor.data_admissao.strftime("%d/%m/%Y"), estilo_celula),
            ],
        ]
        #largura_pagina, altura_pagina = A4
        tabela = Table(dados_tabela, colWidths=[115,200]) #[largura_pagina - 80 - 400, 320]
        tabela.hAlign = "LEFT"
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
            ("LINEAFTER", (0, 0), (0, -1), 0.75, colors.HexColor("#108da5")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEADING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        elementos.append(tabela)
        elementos.append(Spacer(1, 20))

    def _adicionar_resultados(
        self,
        elementos: list,
        resultados: list[ResultadoRegra]
    ):
        elementos.append(
            Paragraph("Resultado da Simulação", self.estilo)
        )
        estilo_celula = ParagraphStyle(
            "CelulaResultado",
            parent=self.styles["BodyText"],
            fontSize=8,
            leading=12,
            alignment=TA_CENTER,
            )
        estilo_celula_negrito = ParagraphStyle(
            "CelulaResultadoNegrito",
            parent=estilo_celula,
            textColor=colors.white,
            alignment=TA_CENTER,
            )

        largura_pagina, altura_pagina = A4

        for resultado in resultados:
            elementos.append(
                Paragraph(resultado.nome, self.styles["Heading2"])
            )

            status = "Cumprida" if resultado.cumpriu else "Não cumprida"

            elementos.append(
                Paragraph(
                    f"<b>Status:</b> {status}",
                    self.styles["BodyText"]
                )
            )

            elementos.append(
                Spacer(1,6)
            )

            if resultado.pendencias:
                pendencias = "<br/>".join(
                    [f"- {pendencia}" for pendencia in resultado.pendencias]
                )
            else:
                pendencias = "Não foram identificadas pendências."

            if resultado.observacoes:
                observacoes = "<br/>".join(
                    [f"- {observacao}" for observacao in resultado.observacoes]
                )
            else:
                observacoes = "-"

            # Mapeamento entre chaves de requisitos e valores_apurados
            mapa_requisitos_valores = {
                "idade_minima": "idade",
                "contribuicao_minima": "anos_total_contribuicao",
                "servico_publico_minimo": "anos_efetivo_exercicio",
                "cargo_minimo": "anos_no_cargo",
                "ingresso_maximo": "data_admissao",
                "idade_compulsoria": "idade",
            }

            # Monta as linhas da tabela: requisito | valor apurado
            linhas_tabela = []
            for chave_requisito, valor_requisito in resultado.requisitos.items():
                chave_valor = mapa_requisitos_valores.get(chave_requisito)
                if chave_valor and chave_valor in resultado.valores_apurados:
                    valor_apurado = resultado.valores_apurados[chave_valor]
                else:
                    valor_apurado = "-"
                linhas_tabela.append(
                    [
                        Paragraph(
                            f"<b>{self._formatar_chave(chave_requisito)}:</b> {valor_requisito}",
                            estilo_celula
                        ),
                        Paragraph(
                            f"<b>{self._formatar_chave(chave_valor)}:</b> {valor_apurado}" if chave_valor else "-",
                            estilo_celula
                        ),
                    ]
                )

            dados_tabela = [
                [
                    Paragraph("<b>Requisitos</b>", estilo_celula_negrito),
                    Paragraph("<b>Valores apurados</b>", estilo_celula_negrito),
                ],
                *linhas_tabela,
            ]
            tabela = Table(
                dados_tabela,
                colWidths=[(largura_pagina/2) - 40, (largura_pagina/2) - 40]
            )

            tabela.hAlign = "CENTER"

            tabela.setStyle(TableStyle([
                # "background", (coluna_inicial, linha_inicial), (coluna_final, linha_final), cor)
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#108da5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.white),
                ("LINEAFTER", (0, 0), (0, -1), 0.75, colors.HexColor("#108da5")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]))
            elementos.append(tabela)

            elementos.append(Spacer(1, 6))

            elementos.append(
                Paragraph(
                    "<b>Pendência:</b>",
                    self.styles["BodyText"]
                )
            )
            elementos.append(
                Paragraph(
                    f"{pendencias}",
                    self.styles["BodyText"]
                )
            )
            elementos.append(
                Paragraph(
                    "<b>Observações:</b>",
                    self.styles["BodyText"]
                )
            )
            elementos.append(
                Paragraph(
                    f"{observacoes}",
                    self.styles["BodyText"]
                )
            )           


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

    @staticmethod
    def _formatar_chave(chave: str) -> str:
        return chave.replace("_", " ").capitalize()