import streamlit as st

from ..config import CAMINHO_JSON
from ..relatorios import PDFGenerator
from ..repositorio import RepositorioServidores
from ..simulador import SimuladorAposentadoria
from .cabecalho import exibir_cabecalho
from .formulario import capturar_dados_tempo, exibir_dados_servidor
from .resultados import exibir_resultados


@st.cache_resource(show_spinner="Carregando base de dados...")
def _carregar_repositorio(caminho: str, modificado_em: float) -> RepositorioServidores:
    # `modificado_em` faz parte da chave do cache: se o JSON for atualizado,
    # a base é recarregada automaticamente.
    return RepositorioServidores(caminho)


class AppPreviaAposentadoria:
    def __init__(self):
        if not CAMINHO_JSON.exists():
            st.error(
                f"Base de dados não encontrada em '{CAMINHO_JSON.name}'. "
                "Gere o arquivo com scripts/converter_json.py."
            )
            st.stop()

        self.repositorio = _carregar_repositorio(
            str(CAMINHO_JSON), CAMINHO_JSON.stat().st_mtime
        )
        self.simulador = SimuladorAposentadoria()
        self.pdf_generator = PDFGenerator()

    def executar(self):
        exibir_cabecalho()

        st.write(
            "Informe o MASP e o número de admissão do servidor "
            "para gerar uma simulação preliminar de aposentadoria."
        )

        col_masp, col_adm = st.columns(2)
        with col_masp:
            masp = st.text_input("MASP")
        with col_adm:
            adm = st.text_input("ADM")

        if not masp or not adm:
            st.info("Informe o MASP e o ADM para iniciar.")
            return

        servidor = self.repositorio.buscar_por_masp_adm(masp, adm)
        if servidor is None:
            st.error("MASP/ADM não encontrado.")
            return

        data_admissao = exibir_dados_servidor(servidor)
        if data_admissao is None:
            st.warning("Informe uma data de admissão válida.")
            st.stop()

        # Usa a data de admissão possivelmente editada pelo usuário em todas
        # as etapas seguintes (cálculo do teto, regras e PDF).
        servidor.data_admissao = data_admissao

        dados_tempo = capturar_dados_tempo(servidor)

        if st.button("Calcular prévia"):
            resultados = self.simulador.simular(servidor, dados_tempo)
            exibir_resultados(resultados)

            caminho_pdf = self.pdf_generator.gerar(servidor, resultados)
            with open(caminho_pdf, "rb") as arquivo:
                st.download_button(
                    label="Baixar PDF da prévia",
                    data=arquivo,
                    file_name=f"previa_aposentadoria_{servidor.masp}.pdf",
                    mime="application/pdf"
                )
