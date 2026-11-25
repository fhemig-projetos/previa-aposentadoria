import streamlit as st

from ..autenticacao import verificar_credenciais
from .cabecalho import exibir_cabecalho


def tela_login():
    exibir_cabecalho()
    st.subheader("Login")

    st.markdown("""
        <style>
            div[data-testid="stTextInput"] {
                max-width: 350px;
            }
        </style>
    """, unsafe_allow_html=True)

    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        try:
            usuarios = st.secrets["usuarios"]
        except (KeyError, FileNotFoundError):
            st.error("Usuários não configurados nos Secrets do Streamlit.")
            return

        if verificar_credenciais(usuario, senha, usuarios):
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")


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
