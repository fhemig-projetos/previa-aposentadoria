import streamlit as st

from ..modelos import ResultadoRegra
from ..utils.formatacao import formatar_chave, formatar_valor


def exibir_resultados(resultados: list[ResultadoRegra]):
    st.subheader("Resultado da prévia")

    total_regras = len(resultados)
    regras_cumpridas = sum(1 for r in resultados if r.cumpriu)
    regras_nao_cumpridas = total_regras - regras_cumpridas

    col_cumpridas, col_nao_cumpridas = st.columns(2)
    col_cumpridas.metric("Regras cumpridas", regras_cumpridas)
    col_nao_cumpridas.metric("Regras não cumpridas", regras_nao_cumpridas)

    st.divider()

    for resultado in resultados:
        _exibir_regra(resultado)


def _exibir_regra(resultado: ResultadoRegra):
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
                st.write(f"**{formatar_chave(chave)}:** {formatar_valor(valor)}")

        with col2:
            st.markdown("#### Requisitos")
            for chave, valor in resultado.requisitos.items():
                st.write(f"**{formatar_chave(chave)}:** {formatar_valor(valor)}")

        if resultado.pendencias:
            st.markdown("#### O que falta cumprir")
            for pendencia in resultado.pendencias:
                st.write(f"• {formatar_valor(pendencia)}")
        else:
            st.success("Não há pendências para esta regra.")

        st.markdown("#### Forma de Provento")
        for provento in resultado.proventos:
            st.write(f"• {provento}")

        st.markdown("#### Data prevista para atendimento dos requisitos")
        if resultado.data_previsao:
            st.write(f"• {resultado.data_previsao.strftime('%d/%m/%Y')}")
        elif resultado.cumpriu:
            st.write("• Requisitos já atendidos.")
        else:
            st.write(
                "• Não foi possível estimar a data de atendimento "
                "dos requisitos."
            )

        if resultado.observacoes:
            with st.expander("Ver observações"):
                for observacao in resultado.observacoes:
                    st.write(f"• {observacao}")
