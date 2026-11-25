from datetime import date

import streamlit as st

from ..modelos import DadosTempo, Servidor

DATA_LIMITE_TETO_INSS = date(2015, 2, 11)


def exibir_dados_servidor(servidor: Servidor) -> date:
    """Mostra os dados funcionais e devolve a data de admissão (editável)."""
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
            f"**Data de Nascimento:** "
            f"{servidor.data_nascimento.strftime('%d/%m/%Y')}"
        )
        st.write(f"**Sexo:** {servidor.sexo}")
        st.write(f"**Idade:** {servidor.idade} anos")

        chave_data_admissao = f"data_admissao_editavel_{servidor.masp}_{servidor.adm}"
        data_admissao = st.date_input(
            "Data de Admissão",
            value=servidor.data_admissao,
            key=chave_data_admissao,
            format="DD/MM/YYYY"
        )

        if data_admissao is not None and data_admissao != servidor.data_admissao:
            st.caption(
                "A data foi alterada manualmente. "
                f"Registro na base: {servidor.data_admissao.strftime('%d/%m/%Y')}"
            )

        st.caption(
            "Se a data de admissão for igual 01/08/1990, o sistema pode ter considerado que o servidor ingressou no serviço público com a implementação do regime estatutário, necessário conferência."
        )

    return data_admissao


def capturar_dados_tempo(servidor: Servidor) -> DadosTempo:
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

        teto_obrigatorio = servidor.data_admissao > DATA_LIMITE_TETO_INSS

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
            options=["Sim", "Não"]
        )
        interrupcao_efetivo_2003 = st.selectbox(
            "O servidor comprova exercício no serviço público em cargo efetivo sem interrupção desde 31/12/2003:",
            options=["Sim", "Não"]
        )
        interrupcao_efetivo_2020 = st.selectbox(
            "O servidor comprova exercício no serviço público em cargo efetivo sem interrupção desde 15/09/2020:",
            options=["Sim", "Não"]
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
        interrupcao_efetivo_2020=(interrupcao_efetivo_2020 == "Sim"),
        ferias_premio=ferias_premio,
        dias_abono=dias_abono
    )
