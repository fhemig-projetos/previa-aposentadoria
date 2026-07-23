import streamlit as st
from datetime import date
import pandas as pd

from codigo import DadosTempo
from codigo import RepositorioServidores
from codigo import SimuladorAposentadoria
from codigo import PDFGenerator
from codigo.converter_json import converter_excel_para_json

st.set_page_config(
    page_title="Prévia de Aposentadoria",
    page_icon="assets/icone.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def exibir_cabecalho():
    col_logo, col_titulo = st.columns([1,7], vertical_alignment="center")
    with col_logo:
        st.image(
            "assets/logoFhemig.png",
            width=180
        )
    with col_titulo:
        st.markdown(
            """
            <h1 style='margin-bottom: 0;'>Prévia de Aposentadoria</h1>
            <p style='font-size: 18px; color: #bdbdbd; margin-top: 0;'>
            Sistema de simulação previdenciária desenvolvido pela Diretoria de Gestão de Pessoas.
            </p>
            """,
            unsafe_allow_html=True
        )
    st.divider()

def tela_login():
    exibir_cabecalho()
    #st.title("Login")
    st.subheader("Login")
    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        try:
            usuarios = st.secrets["usuarios"]
            if usuario in usuarios and senha == usuarios[usuario]:
                st.session_state["autenticado"] = True
                st.session_state["usuario"] = usuario
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
        except KeyError:
            st.error("Usuários não configurados nos Secrets do Streamlit Cloud.")

def verificar_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        tela_login()
        st.stop()

def botao_sair():
    with st.sidebar:
        usuario_logado = st.session_state.get("usuario", "")
        st.write(f"Usuário: {usuario_logado}")

        if st.button("Sair"):
            st.session_state["autenticado"] = False
            st.session_state["usuario"] = ""
            st.rerun()

st.set_page_config(
    page_title="Prévia de Aposentadoria",
    layout="wide"
)


class AppPreviaAposentadoria:
    def __init__(self):
        self._atualizar_base_dados()
        self.repositorio = RepositorioServidores("dados/dados_cadastrais.json")
        self.simulador = SimuladorAposentadoria()
        self.pdf_generator = PDFGenerator()

    def _atualizar_base_dados(self):
        try:
            converter_excel_para_json(
                caminho_excel="dados/dados_cadastrais.xlsx",
                caminho_json="dados/dados_cadastrais.json"
            )
        except Exception as e:
            st.error(
                f"Erro ao carregar bases de dados: {e}"
            )
            st.stop()

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
            st.write(f"**Número de Admissão:** {servidor.adm}")
            st.write(f"**Nome:** {servidor.nome}")
            st.write(f"**Carreira:** {servidor.cargo}")
            st.write(f"**Categoria Profissional:** {servidor.funcao}")

        with col2:
            st.write(
                f"**Data de Admissão:** "
                f"{servidor.data_admissao.strftime('%d/%m/%Y')}"
            )
            st.write(
                f"**Data de Nascimento:** "
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
            #st.write(
            #    f"**Sujeito ao teto do INSS:** "
            #    f"{self.formatar_indefinido(getattr(servidor, 'sujeito_ao_teto_inss', None))}"
            #    )
            
            #st.write(
            #    f"**Dias sem interrupção:** "
            #    f"{self.formatar_indefinido(getattr(servidor, 'interrupcao', None))}"
            #)

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

            demais_dias = st.number_input(
                "Demais dias de contribuição averbados:",
                min_value=0,
                step=1
            )
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

        with col2:

            interrupcao = st.selectbox(
                "O servidor comprova exercício no serviço público sem interrupção desde 16/12/1998:",
                options=[
                    "Sim",
                    "Não"
                ]
            )
            interrupcao_efetivo_2003 = st.selectbox(
                "O servidor comprova exercício no serviço público em cargo efetivo sem interrupção desde 31/12/2003:",
                options=["Sim",
                         "Não"
                ]
            )
            interrupcao_efetivo_2020 = st.selectbox(
                "O servidor comprova exercício no serviço público em cargo efetivo sem interrupção desde 15/09/2020:",
                options=[
                    "Sim",
                    "Não"
                ]
            )
            ferias_premio = st.number_input(
                "Dias de férias prêmio adquiridas até 16/12/1998 a serem contadas em dobro para aposentadoria:",
                min_value=0,
                step=1
            )
            dias_abono = st.number_input(
                "Dias de abono 1.2 ou 1.7 que o servidor possui como consta no campo da Matriz de Apuração de Tempo para Aposentadoria:",
                min_value=0,
                step=1
            )
            

        return DadosTempo(
            dias_efetivo_exercicio=dias_efetivo_exercicio,
            dias_contribuicao_externa=dias_contribuicao_externa,
            dias_no_cargo=dias_no_cargo,
            demais_dias=demais_dias,
            sujeito_ao_teto_inss=(sujeito_ao_teto == "Sim"),
            interrupcao=(interrupcao == "Sim"),
            interrupcao_efetivo_2003=(interrupcao_efetivo_2003 == "Sim"),
            interrupcao_efetivo_2020=(interrupcao_efetivo_2020=="Sim"),
            ferias_premio=ferias_premio,
            dias_abono=dias_abono
        )

    def _formatar_chave(self, chave: str) -> str:
        traducoes = {
            "idade": "Idade",
            #"sexo": "Sexo",
            #"data_nascimento": "Data de nascimento",
            "anos_efetivo_exercicio": "Anos de efetivo exercício",
            "anos_contribuicao_externa": "Anos de contribuição externa",
            "anos_total_contribuicao": "Tempo total de contribuição",
            "anos_no_cargo": "Anos no cargo",
            "anos_na_carreira": "Anos na carreira",

            "idade_minima": "Idade mínima",
            "contribuicao_minima": "Tempo mínimo de contribuição",
            "tempo_minimo_cargo": "Tempo mínimo no cargo",
            "servico_publico_minimo": "Tempo mínimo de serviço público",
            "carreira_minima": "Tempo mínimo na carreira",
            "cargo_minimo": "Tempo mínimo no cargo",
        }
        return traducoes.get(chave, chave.replace("_", " ").capitalize())

    def _exibir_resultados(self, resultados):
        st.subheader("Resultado da prévia")

        total_regras = len(resultados)
        regras_cumpridas = sum(1 for r in resultados if r.cumpriu)
        regras_nao_cumpridas = total_regras - regras_cumpridas

        col2, col3 = st.columns(2)

        col2.metric("Regras cumpridas", regras_cumpridas)
        col3.metric("Regras não cumpridas", regras_nao_cumpridas)

        st.divider()

        for resultado in resultados:
            with st.container(border=True):
                if resultado.cumpriu:
                    st.markdown(f"### ✅ {resultado.nome}")
                    st.success("Esta regra foi cumprida.")
                else:
                    st.markdown(f"### ⚠️ {resultado.nome}")
                    st.warning("Esta regra ainda não foi cumprida.")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Valores apurados")
                    for chave, valor in resultado.valores_apurados.items():
                        st.write(f"**{self._formatar_chave(chave)}:** {valor}")

                with col2:
                    st.markdown("#### Requisitos")
                    for chave, valor in resultado.requisitos.items():
                        st.write(f"**{self._formatar_chave(chave)}:** {valor}")

                if resultado.pendencias:
                    st.markdown("#### O que falta cumprir")
                    for pendencia in resultado.pendencias:
                        st.write(f"• {pendencia}")
                else:
                    st.success("Não há pendências para esta regra.")

                if resultado.observacoes:
                    with st.expander("Ver observações"):
                        for observacao in resultado.observacoes:
                            st.write(f"• {observacao}")


if __name__ == "__main__":
    verificar_login()
    botao_sair()

    app = AppPreviaAposentadoria()
    app.executar()