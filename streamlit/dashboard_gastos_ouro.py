import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração inicial da página
st.set_page_config(
    page_title="Análise de Gastos em Ouro - iFood",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .header-text { 
        color: #000000;
        font-family: 'Arial';
        border-bottom: 2px solid #000000;
        padding-bottom: 10px;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .report-box {
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        background-color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner="Carregando dados...")
def load_data(file_path: str) -> pd.DataFrame:
    """
    Carrega e otimiza os dados do arquivo CSV
    """
    try:
        df = pd.read_csv(
            file_path,
            usecols=['Year_Birth', 'MntGoldProds'],
            dtype={'Year_Birth': 'int16', 'MntGoldProds': 'int32'}
        )
        return df.dropna()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def calculate_age_and_groups(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula idade e cria faixas etárias
    """
    current_year = datetime.now().year
    df['Age'] = current_year - df['Year_Birth']
    
    bins = [20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
    df['Faixa_Etaria'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    return df

def create_gold_spending_plot(df: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de barras interativo
    """
    media_gastos = df.groupby('Faixa_Etaria', observed=False)['MntGoldProds'].mean().reset_index()
    
    fig = px.bar(
        media_gastos,
        x='Faixa_Etaria',
        y='MntGoldProds',
        color='Faixa_Etaria',
        color_discrete_sequence=px.colors.sequential.Darkmint,
        labels={'MntGoldProds': 'Média de Gastos (USD)', 'Faixa_Etaria': 'Faixa Etária'},
        title='Gastos Médios em Produtos de Ouro por Faixa Etária'
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        xaxis_title=None,
        yaxis_title="Média de Gastos (USD)",
        hovermode="x unified"
    )
    
    return fig

import textwrap

def generate_insight_blocks(df: pd.DataFrame):
    """
    Gera três blocos de texto estilizados com insights, média por faixa etária e recomendações.
    """
    media_gastos = df.groupby('Faixa_Etaria', observed=False)['MntGoldProds'].mean()
    max_faixa = media_gastos.idxmax()
    max_value = media_gastos.max()
    variacao = max_value - media_gastos.min()

    # Bloco 1 - Principais Insights
    bloco_1 = f"""
    <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; border:1px solid #ddd; margin-bottom:10px;">
        <p><strong>Padrões de Gastos:</strong></p>
        <ul>
            <li>Faixa etária com maior gasto médio: <strong>{max_faixa}</strong> (USD {max_value:.2f})</li>
            <li>Variação entre faixas etárias: <strong>USD {variacao:.2f}</strong></li>
        </ul>
    </div>
    """

    # Bloco 2 - Média por faixa etária
    bloco_2 = """
    <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; border:1px solid #ddd; margin-bottom:10px;">
        <p><strong>Média de gastos por faixa etária:</strong></p>
        <ul>
    """
    for faixa, valor in media_gastos.items():
        bloco_2 += f"<li>{faixa}: USD {valor:.2f}</li>\n"
    bloco_2 += "</ul></div>"

    # Bloco 3 - Recomendações
    bloco_3 = f"""
    <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; border:1px solid #ddd;">
        <p><strong>Recomendações Estratégicas:</strong></p>
        <ul>
            <li>Desenvolver campanhas direcionadas para clientes entre <strong>{max_faixa}</strong></li>
            <li>Criar bundles exclusivos para faixas etárias específicas</li>
            <li>Implementar programa de fidelidade para clientes de alto gasto</li>
        </ul>
    </div>
    """

    return bloco_1, bloco_2, bloco_3
def main():
    """Função principal do dashboard"""
    st.markdown('<h1 class="header-text">💰 Análise de Gastos em Produtos de Ouro</h1>', unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data('../data/processed/marketing_campaign_atualizado.csv')
    
    if not df.empty:
        # Processamento dos dados
        df = calculate_age_and_groups(df)
        
        # Filtro interativo
        with st.container():
            age_filter = st.slider(
                '🔢 Filtrar por Idade:',
                min_value=int(df['Age'].min()),
                max_value=int(df['Age'].max()),
                value=(20, 100)
            )
        
        # Aplicar filtro
        filtered_df = df[df['Age'].between(*age_filter)]
        
        # Layout principal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico principal
            st.plotly_chart(create_gold_spending_plot(filtered_df), use_container_width=True)
            
        with col2:
            # Métricas rápidas
            st.markdown("### 📊 Métricas Chave")
            total_gasto = filtered_df['MntGoldProds'].sum()
            avg_gasto = filtered_df['MntGoldProds'].mean()
            
            st.markdown(f'<div class="metric-card">Total Gasto: USD {total_gasto:,.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Média Geral: USD {avg_gasto:,.2f}</div>', unsafe_allow_html=True)
        
        # Seção de insights
        st.markdown("---")
        with st.container():
            st.markdown("### 📄 Análise Detalhada")
            bloco_1, bloco_2, bloco_3 = generate_insight_blocks(df)

            st.markdown(bloco_1, unsafe_allow_html=True)
            st.markdown(bloco_2, unsafe_allow_html=True)
            st.markdown(bloco_3, unsafe_allow_html=True)
           
if __name__ == "__main__":
    main()