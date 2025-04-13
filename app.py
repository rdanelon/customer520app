import streamlit as st
import pandas as pd
import plotly.express as px

# Versão 1.0.2 - Melhorias: inclusão de dados por canal (Chat, E-mail, CRM, Telefone)
st.set_page_config(page_title="520@app - Capacidade do Suporte", layout="centered")
st.title("Calculadora de Capacidade da Equipe de Suporte")
st.markdown("Informe os dados abaixo para estimar a capacidade da sua equipe e comparar com a demanda esperada por canal.")

st.header("1. Dados da Equipe")
col1, col2 = st.columns(2)
with col1:
    agentes = st.number_input("Quantidade de Agentes", min_value=1, value=10)
    horas_dia = st.number_input("Horas de trabalho por dia", min_value=1, max_value=24, value=8)
    eficiencia = st.slider("Eficiência da equipe (%)", 50, 100, 85)
with col2:
    dias_uteis = st.number_input("Dias úteis por mês", min_value=1, max_value=31, value=22)
    ocupacao = st.slider("Ocupação desejada (%)", 50, 100, 80)
    senha = st.text_input("Senha de acesso", type="password")

if senha != "suporte25":
    st.warning("Acesso restrito. Digite a senha correta para continuar.")
    st.stop()

# Cálculo de capacidade
minutos_disponiveis = agentes * horas_dia * 60 * dias_uteis
capacidade_total = minutos_disponiveis * (eficiencia / 100) * (ocupacao / 100)

st.success(f"Capacidade total disponível da equipe: **{int(capacidade_total):,} minutos/mês**".replace(",", "."))

st.header("2. Demanda por Canal")
canal_dados = []

canais = ["Chat", "E-mail", "CRM", "Telefone"]
for canal in canais:
    with st.expander(f"{canal}"):
        chamados = st.number_input(f"Chamados por mês - {canal}", min_value=0, value=0, key=f"{canal}_qtd")
        tma = st.number_input(f"TMA médio (min) - {canal}", min_value=1, value=10, key=f"{canal}_tma")
        carga = chamados * tma
        canal_dados.append({
            "Canal": canal,
            "Chamados": chamados,
            "TMA (min)": tma,
            "Carga (min)": carga
        })

# Processamento dos dados
df = pd.DataFrame(canal_dados)
df["% da Carga"] = (df["Carga (min)"] / capacidade_total * 100).round(1)
df["Status"] = df["Carga (min)"].apply(lambda x: "OK" if x <= capacidade_total else "Excede")

carga_total = df["Carga (min)"].sum()

st.header("3. Resultado")

st.subheader("Resumo por Canal")
st.dataframe(df.style.applymap(lambda val: "color: red" if val == "Excede" else "color: green", subset=["Status"]))

st.markdown(f"**Carga total estimada:** {int(carga_total):,} minutos/mês".replace(",", "."))
if carga_total > capacidade_total:
    st.error("A carga estimada excede a capacidade da equipe!")
else:
    st.success("A equipe tem capacidade suficiente para atender a demanda estimada.")

# Gráfico comparativo
grafico_df = df.copy()
grafico_df.loc[len(grafico_df.index)] = ["Capacidade", "-", "-", capacidade_total, 100, "Total"]

fig = px.bar(grafico_df, x="Canal", y="Carga (min)", color="Canal",
             title="Demanda por Canal vs Capacidade Total",
             text="Carga (min)", height=400)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Desenvolvido por Ricardo Danelon - Versão 520@app")
