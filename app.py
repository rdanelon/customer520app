import streamlit as st
import pandas as pd

# Autenticação simples
def autenticar():
    senha = st.text_input("Digite a senha para acessar o app:", type="password")
    if senha != "suporte25":
        st.warning("Acesso negado.")
        st.stop()

# Função principal do app
def main():
    st.set_page_config(page_title="520@app - Capacidade da Equipe", layout="centered")
    autenticar()

    st.title("520@app")
    st.subheader("Cálculo de Capacidade da Equipe de Suporte ao Cliente")

    st.markdown("Preencha os dados abaixo para calcular a capacidade da sua equipe:")

    with st.form("formulario"):
        col1, col2 = st.columns(2)

        with col1:
            total_agentes = st.number_input("Total de agentes disponíveis", min_value=1)
            horas_dia = st.number_input("Horas de trabalho por dia (por agente)", min_value=1)
            dias_uteis = st.number_input("Dias úteis no mês", min_value=1)
        
        with col2:
            eficiencia = st.slider("Eficiência média (%)", 50, 100, 85)
            tma = st.number_input("TMA médio (em minutos)", min_value=1.0)
            ocupacao = st.slider("Ocupação desejada (%)", 50, 100, 85)

        submit = st.form_submit_button("Calcular Capacidade")

    if submit:
        minutos_trabalho = total_agentes * horas_dia * 60 * dias_uteis
        minutos_disponiveis = minutos_trabalho * (eficiencia / 100) * (ocupacao / 100)
        capacidade_total = int(minutos_disponiveis / tma)

        st.success(f"Capacidade estimada de atendimento no mês: **{capacidade_total} chamados**")
        st.caption("Essa estimativa considera a eficiência e ocupação médias definidas.")

# Executa o app
if __name__ == "__main__":
    main()
