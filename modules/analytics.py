import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

class Analytics:
    def __init__(self, database):
        self.db = database
    
    def obter_dados_para_dashboard(self, periodo=None):
        """Prepara dados para o dashboard"""
        boletos = self.db.obter_boletos()
        
        if not boletos:
            return self._dados_vazios()
        
        # Converte para DataFrame para análise
        df = pd.DataFrame(boletos)
        df['vencimento'] = pd.to_datetime(df['vencimento'])
        df['valor'] = pd.to_numeric(df['valor'])
        
        # Aplica filtro de período se especificado
        if periodo:
            df = self._filtrar_por_periodo(df, periodo)
        
        return self._processar_dados(df)
    
    def _filtrar_por_periodo(self, df, periodo):
        """Filtra dados por período"""
        hoje = datetime.now()
        
        if periodo == 'este_mes':
            inicio_mes = hoje.replace(day=1)
            return df[df['vencimento'] >= inicio_mes]
        
        elif periodo == 'proxima_semana':
            fim_semana = hoje + timedelta(days=7)
            return df[(df['vencimento'] >= hoje) & (df['vencimento'] <= fim_semana)]
        
        elif periodo == 'atrasados':
            return df[df['status'] == 'atrasado']
        
        return df
    
    def _processar_dados(self, df):
        """Processa os dados para o dashboard"""
        # Estatísticas básicas
        total_boletos = len(df)
        total_pendentes = len(df[df['status'].isin(['pendente', 'atrasado'])])
        total_atrasados = len(df[df['status'] == 'atrasado'])
        total_pagos = len(df[df['status'] == 'pago'])
        
        # Valores financeiros
        total_a_pagar = df[df['status'].isin(['pendente', 'atrasado'])]['valor'].sum()
        total_pago = df[df['status'] == 'pago']['valor'].sum()
        valor_atrasado = df[df['status'] == 'atrasado']['valor'].sum()
        
        # Análise por categoria
        gastos_por_categoria = df.groupby('categoria')['valor'].sum().sort_values(ascending=False)
        
        # Próximos vencimentos
        hoje = datetime.now()
        proximos_7_dias = hoje + timedelta(days=7)
        boletos_proximos = df[
            (df['status'].isin(['pendente'])) & 
            (df['vencimento'] <= proximos_7_dias) & 
            (df['vencimento'] >= hoje)
        ].sort_values('vencimento')
        
        return {
            'estatisticas': {
                'total_boletos': total_boletos,
                'total_pendentes': total_pendentes,
                'total_atrasados': total_atrasados,
                'total_pagos': total_pagos,
                'total_a_pagar': total_a_pagar,
                'total_pago': total_pago,
                'valor_atrasado': valor_atrasado
            },
            'categorias': gastos_por_categoria,
            'proximos_vencimentos': boletos_proximos,
            'boletos_recentes': df.sort_values('data_cadastro', ascending=False).head(5)
        }
    
    def _dados_vazios(self):
        """Retorna estrutura vazia para quando não há dados"""
        return {
            'estatisticas': {
                'total_boletos': 0,
                'total_pendentes': 0,
                'total_atrasados': 0,
                'total_pagos': 0,
                'total_a_pagar': 0,
                'total_pago': 0,
                'valor_atrasado': 0
            },
            'categorias': pd.Series(),
            'proximos_vencimentos': pd.DataFrame(),
            'boletos_recentes': pd.DataFrame()
        }
    
    def criar_grafico_pizza_categorias(self, categorias):
        """Cria gráfico de pizza para gastos por categoria - VERSÃO CORRIGIDA"""
        try:
            if categorias.empty or len(categorias) == 0:
                fig = go.Figure()
                fig.add_annotation(
                    text="📊 Nenhum dado disponível", 
                    x=0.5, y=0.5, 
                    showarrow=False,
                    font=dict(size=16)
                )
                fig.update_layout(
                    title="Gastos por Categoria",
                    height=400
                )
                return fig
            
            # ✅ CORREÇÃO: Converter numpy para float padrão
            valores = [float(val) for val in categorias.values]
            nomes = categorias.index.tolist()
            
            fig = px.pie(
                values=valores,
                names=nomes,
                title="📊 Gastos por Categoria",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}'
            )
            fig.update_layout(height=400)
            return fig
            
        except Exception as e:
            print(f"❌ Erro no gráfico pizza: {e}")
            fig = go.Figure()
            fig.add_annotation(text="❌ Erro no gráfico", x=0.5, y=0.5, showarrow=False)
            fig.update_layout(height=400)
            return fig
    
    def criar_grafico_barras_status(self, estatisticas):
        """Cria gráfico de barras para status dos boletos - VERSÃO CORRIGIDA"""
        try:
            # ✅ CORREÇÃO: Converter numpy para float padrão
            status_data = {
                'Status': ['Pendentes', 'Atrasados', 'Pagos'],
                'Quantidade': [
                    int(estatisticas['total_pendentes']),
                    int(estatisticas['total_atrasados']), 
                    int(estatisticas['total_pagos'])
                ],
                'Valor (R$)': [
                    float(estatisticas['total_a_pagar']),
                    float(estatisticas['valor_atrasado']),
                    float(estatisticas['total_pago'])
                ]
            }
            
            df = pd.DataFrame(status_data)
            fig = px.bar(
                df, 
                x='Status', 
                y='Quantidade',
                text='Quantidade',
                title="📈 Boletos por Status",
                color='Status',
                color_discrete_map={
                    'Pendentes': '#FFA726',
                    'Atrasados': '#EF5350', 
                    'Pagos': '#66BB6A'
                }
            )
            fig.update_layout(
                showlegend=False,
                height=400,
                yaxis_title="Quantidade de Boletos"
            )
            fig.update_traces(
                hovertemplate='<b>%{x}</b><br>Quantidade: %{y}<br>Valor: R$ %{customdata:,.2f}',
                customdata=df['Valor (R$)']
            )
            return fig
            
        except Exception as e:
            print(f"❌ Erro no gráfico barras: {e}")
            fig = go.Figure()
            fig.add_annotation(text="❌ Erro no gráfico", x=0.5, y=0.5, showarrow=False)
            fig.update_layout(height=400)
            return fig