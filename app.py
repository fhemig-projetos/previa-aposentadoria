"""Ponto de entrada do aplicativo (streamlit run app.py)."""

import streamlit as st

from codigo.config import ICONE_PAGINA
from codigo.ui.app_previa import AppPreviaAposentadoria
from codigo.ui.login import botao_sair, verificar_login

# Deve ser o primeiro comando Streamlit do script e ser chamado uma única vez.
st.set_page_config(
    page_title="Prévia de Aposentadoria",
    page_icon=str(ICONE_PAGINA) if ICONE_PAGINA.exists() else None,
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    verificar_login()
    botao_sair()
    AppPreviaAposentadoria().executar()


if __name__ == "__main__":
    main()
