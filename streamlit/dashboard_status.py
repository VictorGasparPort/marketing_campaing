# app_gastos_carne_estado_civil.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import ttest_ind

# ============================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO
# ============================
st.set_page_config(
    page_title="📊 Gastos em Carne por Estado Civil",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para uma estética clean em preto e branco com espaçamentos adequados
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #fff;
            color: #000;
        }
        .report-box {
            background-color: #f9f9f9;
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
            border-left: 5px solid #333;
            line-height: 1.6;
            font-size: 16px;
        }
        h1, h2, h3 {
            color: #000;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================
# 2. CARREGAMENTO DOS DADOS COM CACHE
# ============================
@st.cache_data(show_spinner=True)
def load_data(path: str) -> pd.DataFrame:
    """
    Carrega os dados do CSV com cache para melhor performance.

    Parâmetros:
      - path (str): Caminho do arquivo CSV.

    Retorna:
      - pd.DataFrame: DataFrame com os dados carregados.
    """
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

# ============================
# 3. FUNÇÃO DE ANÁLISE: GASTOS EM CARNE POR ESTADO CIVIL
# ============================
def analisar_gastos_carne_por_estado_civil(dados: pd.DataFrame):
    """
    Analisa a relação entre o estado civil e os gastos em produtos de carne, controlando pela renda.
    
    A função:
      - Verifica a presença de colunas necessárias;
      - Remove linhas com valores nulos;
      - Gera gráficos interativos para:
          • Distribuição dos gastos em carne por estado civil;
          • Distribuição da renda por estado civil;
          • Relação entre renda e gastos em carne.
      - Compara os grupos "Single" e "Married" usando um teste t (t-test)
      - Retorna um dicionário com os principais insights (médias, estatísticas do teste)
    
    Parâmetros:
      - dados (pd.DataFrame): Dados dos clientes.
      
    Retorna:
      - insights (dict): Dicionário com resultados do teste e médias.
      - df_limpo (pd.DataFrame): DataFrame processado para os gráficos.
    """
    # Colunas necessárias
    colunas_necessarias = ['Marital_Status', 'MntMeatProducts', 'Income']
    for coluna in colunas_necessarias:
        if coluna not in dados.columns:
            raise ValueError(f"A coluna '{coluna}' não está presente no DataFrame.")

    # Remover linhas com valores nulos
    df_limpo = dados.dropna(subset=colunas_necessarias).copy()
    
    # --- Gráfico 1: Boxplot de Gastos em Carne por Estado Civil ---
    # Criamos um gráfico interativo com Plotly Express para visualizar a distribuição dos gastos.
    fig_gastos = px.box(df_limpo, x='Marital_Status', y='MntMeatProducts', 
                        color='Marital_Status',
                        title='Distribuição dos Gastos em Produtos de Carne por Estado Civil',
                        labels={'Marital_Status': 'Estado Civil', 'MntMeatProducts': 'Gastos em Produtos de Carne'},
                        color_discrete_sequence=px.colors.sequential.Blugrn)
    fig_gastos.update_layout(template="simple_white", height=500)
    
    # --- Gráfico 2: Boxplot de Renda por Estado Civil ---
    fig_renda = px.box(df_limpo, x='Marital_Status', y='Income', 
                       color='Marital_Status',
                       title='Distribuição da Renda por Estado Civil',
                       labels={'Marital_Status': 'Estado Civil', 'Income': 'Renda'},
                       color_discrete_sequence=px.colors.sequential.Blues)
    fig_renda.update_layout(template="simple_white", height=500)
    
    # --- Gráfico 3: Scatter Plot de Renda vs Gastos em Carne ---
    fig_scatter = px.scatter(df_limpo, x='Income', y='MntMeatProducts', color='Marital_Status',
                             title='Relação entre Renda e Gastos em Produtos de Carne por Estado Civil',
                             labels={'Income': 'Renda', 'MntMeatProducts': 'Gastos em Produtos de Carne'},
                             color_discrete_sequence=px.colors.sequential.Reds)
    fig_scatter.update_layout(template="simple_white", height=500)
    
    # Separar os grupos para o teste estatístico
    grupo_solteiros = df_limpo[df_limpo['Marital_Status'] == 'Single']['MntMeatProducts']
    grupo_casados = df_limpo[df_limpo['Marital_Status'] == 'Married']['MntMeatProducts']
    
    # Teste t (variâncias não iguais)
    t_stat, p_value = ttest_ind(grupo_solteiros, grupo_casados, equal_var=False)
    
    # Preparar insights: calcular médias de gastos em carne para solteiros e casados
    insights = {
        'media_solteiros': grupo_solteiros.mean(),
        'media_casados': grupo_casados.mean(),
        't_stat': t_stat,
        'p_value': p_value
    }
    
    return df_limpo, fig_gastos, fig_renda, fig_scatter, insights

# ============================
# 4. EXECUÇÃO DO DASHBOARD
# ============================
def main():
    # Caminho dos dados
    data_path = '../data/processed/marketing_campaign_atualizado.csv'
    dados = load_data(data_path)
    
    # Interrompe se os dados não forem carregados
    if dados.empty:
        st.stop()
    
    # Cabeçalho do Dashboard
    st.markdown("<h1>📊 Análise de Gastos em Carne por Estado Civil</h1>", unsafe_allow_html=True)
    st.markdown("Este dashboard analisa como o estado civil influencia os gastos em produtos de carne, considerando também a distribuição da renda.")
    st.markdown("---")
    
    # Widget: Dropdown para filtrar por estado civil (opcional)
    opcoes_estados = ['Todos'] + sorted(dados['Marital_Status'].dropna().unique().tolist())
    estado_selecionado = st.selectbox("Filtrar por Estado Civil (opcional):", options=opcoes_estados, index=0)
    
    # Se o usuário escolher um estado específico, filtra os dados
    if estado_selecionado != 'Todos':
        dados = dados[dados['Marital_Status'] == estado_selecionado]
    
    # Widget: Slider para filtrar os dados pela renda
    # Define o mínimo e máximo da coluna 'Income' para o slider
    min_renda = float(dados['Income'].min())
    max_renda = float(dados['Income'].max())
    renda_range = st.slider("Filtrar clientes por faixa de renda:", min_value=int(min_renda), max_value=int(max_renda), 
                            value=(int(min_renda), int(max_renda)), step=100)
    # Filtra o DataFrame conforme o intervalo de renda selecionado
    dados = dados[(dados['Income'] >= renda_range[0]) & (dados['Income'] <= renda_range[1])]
    
    # Aplicar a função de análise e capturar os gráficos e insights
    try:
        df_limpo, fig_gastos, fig_renda, fig_scatter, insights = analisar_gastos_carne_por_estado_civil(dados)
    except Exception as e:
        st.error(f"Erro na análise: {e}")
        st.stop()
    
    # Layout responsivo: Organiza os gráficos em um grid de duas colunas
    st.markdown("## 📈 Visualizações Interativas")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig_gastos, use_container_width=True)
        st.plotly_chart(fig_renda, use_container_width=True)
    with col2:
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Gerar o relatório executivo baseado nos insights obtidos
    st.markdown("## 📝 Relatório Executivo")
    relatorio = f"""
    Médias de Gastos em Produtos de Carne:
    - Solteiros: **{insights['media_solteiros']:.2f}**
    - Casados: **{insights['media_casados']:.2f}**

    Teste Estatístico:
    - t-statistic: **{insights['t_stat']:.2f}**
    - p-value: **{insights['p_value']:.4f}**

    Conclusão:
    """
    if insights['p_value'] < 0.05:
        relatorio += ("Existe uma diferença estatisticamente significativa entre os gastos em carne de solteiros e casados. " 
                      "Sugere-se focar campanhas de marketing direcionadas para o grupo que apresenta maior gasto, "
                      "explorando estratégias que evidenciem os benefícios dos produtos de carne.")
    else:
        relatorio += ("Não foi encontrada uma diferença estatisticamente significativa entre os grupos. "
                      "Recomenda-se revisar as estratégias de marketing e realizar pesquisas adicionais para entender melhor as preferências dos clientes.")
    
    # Exibe o relatório em uma caixa estilizada
    st.markdown(f"<div class='report-box'>{relatorio.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)

# Execução do dashboard com tratamento global de exceções
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
