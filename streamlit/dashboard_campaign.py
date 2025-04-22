import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import ttest_ind
from datetime import datetime

# Configuração inicial da página
st.set_page_config(
    page_title="Análise de Reclamações vs Fidelidade",
    page_icon="📊",
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
    Carrega e processa os dados com tratamento de erros
    """
    try:
        df = pd.read_csv(file_path)
        
        # Verificar colunas necessárias
        required_columns = ['Complain', 'Dt_Customer', 'MntWines', 'MntFruits',
                           'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
        
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Colunas necessárias não encontradas no dataset")
            
        # Calcular MntRegularProds se necessário
        if 'MntRegularProds' not in df.columns:
            df['MntRegularProds'] = df[['MntWines', 'MntFruits', 'MntMeatProducts',
                                      'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']].sum(axis=1)
        
        # Processamento adicional
        df['Ano_Inscricao'] = pd.to_datetime(df['Dt_Customer']).dt.year
        df = df.dropna(subset=['Complain', 'Dt_Customer', 'MntRegularProds'])
        
        return df[['Complain', 'Ano_Inscricao', 'MntRegularProds']]
    
    except Exception as e:
        st.error(f"Erro no carregamento de dados: {str(e)}")
        return pd.DataFrame()

def create_complaint_plot(df: pd.DataFrame) -> go.Figure:
    """
    Cria gráfico de distribuição de reclamações
    """
    fig = px.histogram(
        df,
        x='Ano_Inscricao',
        color='Complain',
        nbins=len(df['Ano_Inscricao'].unique()),
        color_discrete_map={0: '#333333', 1: '#666666'},
        labels={'Ano_Inscricao': 'Ano de Inscrição', 'count': 'Número de Clientes'},
        title='Distribuição de Reclamações por Ano de Inscrição'
    )
    
    fig.update_layout(
        barmode='group',
        legend_title_text='Reclamou',
        plot_bgcolor='white',
        xaxis_title="Ano de Inscrição",
        yaxis_title="Contagem de Clientes",
        hovermode="x unified"
    )
    
    fig.for_each_trace(lambda t: t.update(name='Não Reclamou' if t.name == '0' else 'Reclamou'))
    
    return fig

def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calcula métricas principais e teste estatístico
    """
    grupo_reclamaram = df[df['Complain'] == 1]['MntRegularProds']
    grupo_nao_reclamaram = df[df['Complain'] == 0]['MntRegularProds']
    
    t_stat, p_value = ttest_ind(grupo_reclamaram, grupo_nao_reclamaram, equal_var=False)
    
    return {
        'media_reclamaram': grupo_reclamaram.mean(),
        'media_nao_reclamaram': grupo_nao_reclamaram.mean(),
        't_stat': t_stat,
        'p_value': p_value,
        'total_clientes': len(df),
        'taxa_reclamacoes': df['Complain'].mean()
    }

def generate_insights(metrics: dict) -> str:
    """
    Gera relatório textual com insights
    """
    insights = f"""
    ### 📌 Análise Detalhada

    **Métricas Principais:**
    - Clientes que reclamaram: {metrics['media_reclamaram']:.2f} (média de gastos)
    - Clientes que não reclamaram: {metrics['media_nao_reclamaram']:.2f}
    - Diferença: {abs(metrics['media_reclamaram'] - metrics['media_nao_reclamaram']):.2f}
    - Valor-p: {metrics['p_value']:.4f}

    **Interpretação Estatística:**
    {f"✅ Diferença significativa (p < 0.05)" if metrics['p_value'] < 0.05 else "❌ Diferença não significativa"}

    **Recomendações Estratégicas:**
    """
    
    if metrics['p_value'] < 0.05:
        insights += """
    - Priorizar análise das causas das reclamações
    - Implementar programa de recuperação de clientes
    - Desenvolver campanhas especiais para reclamantes"""
    else:
        insights += """
    - Reforçar programas de fidelidade
    - Melhorar processos de atendimento
    - Monitorar indicadores continuamente"""
    
    return insights

def main():
    """Função principal do dashboard"""
    st.markdown('<h1 class="header-text">📊 Análise de Reclamações vs Fidelidade</h1>', unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data('../data/processed/marketing_campaign_atualizado.csv')
    
    if not df.empty:
        # Filtros interativos
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                year_range = st.slider(
                    '🔢 Selecione o intervalo de anos:',
                    min_value=int(df['Ano_Inscricao'].min()),
                    max_value=int(df['Ano_Inscricao'].max()),
                    value=(int(df['Ano_Inscricao'].min()), int(df['Ano_Inscricao'].max()))
                )
            
            with col2:
                complaint_filter = st.selectbox(
                    '📊 Filtrar por status de reclamação:',
                    options=['Todos', 'Reclamaram', 'Não Reclamaram']
                )
        
        # Aplicar filtros
        filtered_df = df[df['Ano_Inscricao'].between(*year_range)]
        if complaint_filter == 'Reclamaram':
            filtered_df = filtered_df[filtered_df['Complain'] == 1]
        elif complaint_filter == 'Não Reclamaram':
            filtered_df = filtered_df[filtered_df['Complain'] == 0]

        # Layout principal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico principal
            st.plotly_chart(create_complaint_plot(filtered_df), use_container_width=True)
            
        with col2:
            # Métricas rápidas
            metrics = calculate_metrics(filtered_df)
            
            st.markdown("### 📈 Métricas Chave")
            st.markdown(f"""
                <div class="metric-card">
                    <h3>👥 Total Clientes</h3>
                    <h2>{metrics['total_clientes']}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <h3>📉 Taxa de Reclamações</h3>
                    <h2>{metrics['taxa_reclamacoes']:.1%}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="metric-card">
                    <h3>📌 Valor-p</h3>
                    <h2>{metrics['p_value']:.4f}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        # Seção de insights
        with st.container():
            st.markdown("---")
            st.markdown(generate_insights(metrics), unsafe_allow_html=True)

if __name__ == "__main__":
    main()