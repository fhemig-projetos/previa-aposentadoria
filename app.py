import streamlit as st
from datetime import date

from codigo import DadosTempo
from codigo import RepositorioServidores
from codigo import SimuladorAposentadoria
from codigo import PDFGenerator


st.set_page_config(
    page_title="Prévia de Aposentadoria",
    layout="wide"
)


class AppPreviaAposentadoria:
    def __init__(self):
        self.repositorio = RepositorioServidores("dados/dados_cadastrais.xlsx")
        self.simulador = SimuladorAposentadoria()
        self.pdf_generator = PDFGenerator()

    def executar(self):
        st.title("Prévia de Aposentadoria")

        st.write(
            "Informe o MASP e ADM do servidor e os dados complementares "
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

        self._exibir_dados_servidor(servidor)

        dados_tempo = self._capturar_dados_tempo(servidor)

        if st.button("Calcular prévia"):
            resultados = self.simulador.simular(servidor, dados_tempo)

            self._exibir_resultados(resultados)

            caminho_pdf = self.pdf_generator.gerar(servidor, resultados)

            with open(caminho_pdf, "rb") as arquivo:
                st.download_button(
                    label="Baixar PDF da prévia",
                    data=arquivo,
                    file_name=f"previa_aposentadoria_{servidor.masp}.pdf",
                    mime="application/pdf"
                )

    def formatar_indefinido(self,valor):
        if valor is True:
            return "Sim"
        if valor is False:
            return "Não"
        return "Não informado"

    def _exibir_dados_servidor(self, servidor):
        st.subheader("Dados funcionais")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**MASP:** {servidor.masp}")
            st.write(f"**ADM:** {servidor.adm}")
            st.write(f"**Nome:** {servidor.nome}")
            st.write(f"**Cargo:** {servidor.cargo}")
            st.write(f"**Função:** {servidor.funcao}")

        with col2:
            st.write(
                f"**Data de admissão:** "
                f"{servidor.data_admissao.strftime('%d/%m/%Y')}"
            )
            st.write(
                f"**Data de nascimento:** "
                f"{servidor.data_nascimento.strftime('%d/%m/%Y')}"
            )
            st.write(
                f"**Sexo:** "
                f"{servidor.sexo}"
            )
            st.write(
                f"**Idade:** "
                f"{servidor.idade} anos"
            )
            st.write(
                f"**Sujeito ao teto do INSS:** "
                f"{self.formatar_indefinido(getattr(servidor, 'sujeito_ao_teto_inss', None))}"
                )
            )
            st.write(
                f"**Dias sem interrupção:** "
                f"{'Sim' if servidor.dias_sem_interrupcao else 'Não'}"
            )

    def _capturar_dados_tempo(self, servidor) -> DadosTempo:
        st.subheader("Informações complementares")

        col1, col2 = st.columns(2)

        with col1:
            dias_efetivo_exercicio = st.number_input(
                "Dias trabalhados no serviço público, como consta na FIPA:",
                min_value=0,
                step=1
            )
            dias_contribuicao_externa = st.number_input(
                "Dias de contribuição averbado do INSS exclusivamente na iniciativa privada:",
                min_value=0,
                step=1
            )

            dias_no_cargo = st.number_input(
                "Dias de efetivo exercício no cargo que se dará a aposentadoria, como consta na FIPA:",
                min_value=0,
                step=1
            )

            dias_na_carreira = st.number_input(
                "Demais dias de contribuição averbados:",
                min_value=0,
                step=1
            )
            

        with col2:
            data_limite = date(2015, 2, 11)
            teto_obrigatorio = servidor.data_admissao > data_limite

            if teto_obrigatorio:
                sujeito_ao_teto = st.selectbox(
                    "Sujeito ao teto do INSS:",
                    options=["Sim"],
                    disabled=True
                )
            else:
                sujeito_ao_teto = st.selectbox(
                    "Sujeito ao teto do INSS:",
                    options=["Sim", "Não"]
                )

            st.caption(
                "Servidor que ingressou no serviço público a partir de 12/02/2015 "
                "obrigatoriamente está sujeito ao teto do INSS, já para os servidores "
                "que ingressaram antes de 12/02/2015 é opcional escolher contribuir "
                "até o valor do teto do INSS."
            )
            interrupcao = st.selectbox(
                "O servidor comprova exercício no serviço público sem interrupção desde 16/12/1998:",
                options=[
                    "Sim",
                    "Não"
                ]
            )
            interrupcao_efetivo = st.selectbox(
                "O servidor comprova exercício no serviço público em cargo efetivo sem interrupção desde 31/12/2003:",
                options=["Sim",
                         "Não"]
            )
            

        return DadosTempo(
            dias_efetivo_exercicio=dias_efetivo_exercicio,
            dias_contribuicao_externa=dias_contribuicao_externa,
            dias_no_cargo=dias_no_cargo,
            dias_na_carreira=dias_na_carreira,
            sujeito_ao_teto_inss=(sujeito_ao_teto == "Sim"),
            interrupcao=(interrupcao == "Sim"),
            interrupcao_efetivo=(interrupcao_efetivo == "Sim")
        )

    def _exibir_resultados(self, resultados):
        st.subheader("Resultado da prévia")

        for resultado in resultados:
            with st.expander(resultado.nome, expanded=True):
                if resultado.cumpriu:
                    st.success("Regra cumprida.")
                else:
                    st.warning("Regra não cumprida.")

                st.write("**Valores apurados:**")
                st.json(resultado.valores_apurados)

                st.write("**Requisitos:**")
                st.json(resultado.requisitos)

                if resultado.pendencias:
                    st.write("**Pendências:**")
                    for pendencia in resultado.pendencias:
                        st.write(f"- {pendencia}")
                else:
                    st.write("Nenhuma pendência identificada.")

                if resultado.observacoes:
                    st.write("**Observações:**")
                    for observacao in resultado.observacoes:
                        st.write(f"- {observacao}")


if __name__ == "__main__":
    app = AppPreviaAposentadoria()
    app.executar()