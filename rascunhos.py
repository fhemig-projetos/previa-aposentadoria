def exibir_cabecalho():
    col_logo, col_titulo = st.columns(
        [1, 6],
        vertical_alignment="center"
    )

    with col_logo:
        st.image("assets/logo_instituicao.png", width=90)

    with col_titulo:
        st.markdown(
            """
            <div style="line-height: 1.2;">
                <h1 style="margin: 0; padding: 0;">
                    Prévia de Aposentadoria
                </h1>
                <p style="
                    margin: 4px 0 0 0;
                    padding: 0;
                    font-size: 18px;
                    color: #666;
                ">
                    Sistema de simulação previdenciária
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()



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