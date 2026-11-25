import streamlit as st

from ..config import LOGO_INTERFACE


def exibir_cabecalho():
    col_logo, col_titulo = st.columns([1, 7], vertical_alignment="center")

    with col_logo:
        if LOGO_INTERFACE.exists():
            st.image(str(LOGO_INTERFACE), width=180)

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
