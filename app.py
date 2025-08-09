import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="@memoraidan",
    page_icon="logo_aidan.png",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/brnftn/aidan/c2244f21864d428ae8d03cb6e758a1631eecb420/ESTOQUE%20AIDAN%20(dash)%20-%20BASE.csv")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Familia Olfativa
familias_disponiveis = sorted(df['Família Olfativa'].dropna().astype(str).unique())
familias_selecionados = st.sidebar.multiselect("Família Olfativa", familias_disponiveis, default=familias_disponiveis)

# Filtro de Tipo
tipos_disponiveis = sorted(df['Tipo'].unique())
tipos_selecionadas = st.sidebar.multiselect("Tipo", tipos_disponiveis, default=tipos_disponiveis)

# Filtro por Valor
precos_disponiveis = sorted(df['Preço Unitário'].unique())
precos_selecionados = st.sidebar.multiselect("Valor", precos_disponiveis, default=precos_disponiveis)

# Filtro por Produto
produtos_disponiveis = sorted(df['Nome do item'].unique())
produtos_selecionados = st.sidebar.multiselect("Produto", produtos_disponiveis, default=produtos_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['Família Olfativa'].isin(familias_selecionados)) &
    (df['Tipo'].isin(tipos_selecionadas)) &
    (df['Preço Unitário'].isin(precos_selecionados)) &
    (df['Nome do item'].isin(produtos_selecionados))
]

# --- Conteúdo Principal ---
st.title("Catálogo online Aidan")
st.markdown("Explore os produtos e consulte a disponibilidade para pronta entrega.  Utilize os filtros à esquerda.")

# --- Métricas Principais (KPIs) ---
#st.subheader("Métricas gerais (Salário anual em USD)")

if not df.empty:
    total_produtos = 32
    total_disponiveis = 23
    forma_pagamento = "Pix"
else:
    total_produtos, total_disponiveis, forma_pagamento = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de produtos cadastrados", total_produtos)
col2.metric("Produtos disponíveis em estoque", total_disponiveis)
col4.metric("Forma de Pagamento", forma_pagamento)

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

# Gráfico de barras: quantidade de produtos por categoria
with col_graf1:
    if not df.empty:
        produtos_categoria = df["Família Olfativa"].value_counts().reset_index()
        produtos_categoria.columns = ["Categoria", "Quantidade"]

        grafico_categoria = px.bar(
            produtos_categoria,
            x="Categoria",
            y="Quantidade",
            title="Quantidade de produtos por categoria",
            labels={"Quantidade": "Quantidade de produtos", "Categoria": "Categoria"},
            color="Quantidade",
        )
        grafico_categoria.update_layout(title_x=0.1)
        st.plotly_chart(grafico_categoria, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de categorias.")

# Gráfico de pizza: distribuição por disponibilidade (estoque > 0)
with col_graf2:
    if not df.empty:
        df["Disponível"] = df["Estoque"].apply(lambda x: "Sim" if x > 0 else "Não")
        disponibilidade = df["Disponível"].value_counts().reset_index()
        disponibilidade.columns = ["Disponível", "Quantidade"]

        grafico_disponibilidade = px.pie(
            disponibilidade,
            names="Disponível",
            values="Quantidade",
            title="Distribuição de disponibilidade de estoque",
            hole=0.5
        )
        grafico_disponibilidade.update_traces(textinfo="percent+label")
        grafico_disponibilidade.update_layout(title_x=0.1)
        st.plotly_chart(grafico_disponibilidade, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de disponibilidade.")

# Histograma: distribuição de preços
if not df.empty:
    grafico_precos = px.histogram(
        df,
        x="Preço Unitário",
        nbins=10,
        title="Distribuição de preços dos produtos",
        labels={"Preço Unitário": "Preço (R$)", "count": "Quantidade"}
    )
    grafico_precos.update_layout(title_x=0.1)
    st.plotly_chart(grafico_precos, use_container_width=True)
else:
    st.warning("Nenhum dado para exibir no histograma de preços.")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
     