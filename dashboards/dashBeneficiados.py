from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash
import plotly.graph_objs as go
import pandas as pd
import requests

# Função para carregar dados de autorizadores do servidor Flask
def load_dados_autorizador():
    try:
        response = requests.get('http://127.0.0.1:5000/dados_autorizador')
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao carregar dados de autorizadores: {e}")
        return []
    except ValueError as e:
        print(f"Erro ao converter dados para JSON: {e}")
        return []

# Função para carregar dados de beneficiados do servidor Flask
def load_dados_beneficiado():
    try:
        response = requests.get('http://127.0.0.1:5000/dados_beneficiado')
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao carregar dados de beneficiados: {e}")
        return []
    except ValueError as e:
        print(f"Erro ao converter dados para JSON: {e}")
        return []

# Função para combinar dados de beneficiados e autorizadores
def combinar_dados():
    beneficiados = load_dados_beneficiado()
    autorizadores = load_dados_autorizador()

    df_beneficiado = pd.DataFrame(beneficiados)
    df_autorizador = pd.DataFrame(autorizadores)

    # Combinar DataFrames
    df_combinado = pd.merge(df_beneficiado, df_autorizador, left_on='id_autorizador', right_on='id', how='left')
    return df_combinado

def create_dashboard_beneficiado(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard_beneficiado/')

    app.title = "Dashboard de Beneficiados"

    # Layout da aplicação
    app.layout = html.Div(className='dashboard-container', children=[
        html.H1(children='Dashboard de Beneficiados'),

        # Filtros
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
                dcc.Dropdown(
                    id='beneficiado-dropdown',
                    placeholder="Selecione um beneficiado",
                    className='dcc-dropdown'
                ),
            ]),
            html.Div(className='four columns', children=[
                dcc.Dropdown(
                    id='tamanho-fralda-dropdown',
                    placeholder="Selecione um tamanho de fralda",
                    className='dcc-dropdown'
                ),
            ]),
            html.Div(className='four columns', children=[
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date_placeholder_text="Data de início",
                    end_date_placeholder_text="Data de término",
                    display_format='MMM Y'
                )
            ])
        ]),

        # Tabelas
        html.Div(className='row', children=[
            html.Div(className='twelve columns', children=[
                html.H3("Quantidade Total de Fraldas por Beneficiado"),
                dash_table.DataTable(
                    id='tabela-quantidade-fraldas',
                    columns=[],
                    data=[],
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'height': 'auto',
                        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                        'whiteSpace': 'normal'
                    },
                )
            ])
        ]),

        # Gráficos em linhas de duas colunas
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dcc.Graph(id='grafico-fraldas-tamanho', className='dcc-graph')
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(id='grafico-fraldas-mes', className='dcc-graph')
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='twelve columns', children=[
                dcc.Graph(id='grafico-marcas-fraldas', className='dcc-graph')
            ])
        ])
    ])

    @app.callback(
        [Output('beneficiado-dropdown', 'options'),
         Output('tamanho-fralda-dropdown', 'options')],
        [Input('beneficiado-dropdown', 'value')]
    )
    def update_dropdown_options(_):
        df = combinar_dados()
        print(f"Colunas do DataFrame: {df.columns}")

        opcoes_beneficiados = [{'label': 'Todos os Beneficiados', 'value': 'all'}] + [{'label': beneficiado, 'value': beneficiado} for beneficiado in df['nome_beneficiado'].unique()]
        opcoes_tamanho_fralda = [{'label': 'Todos os Tamanhos', 'value': 'all'}] + [{'label': tamanho, 'value': tamanho} for tamanho in df['tamanho_liberado'].unique()]

        return opcoes_beneficiados, opcoes_tamanho_fralda

    @app.callback(
        [Output('tabela-quantidade-fraldas', 'data'),
         Output('tabela-quantidade-fraldas', 'columns'),
         Output('grafico-fraldas-tamanho', 'figure'),
         Output('grafico-fraldas-mes', 'figure'),
         Output('grafico-marcas-fraldas', 'figure')],
        [Input('beneficiado-dropdown', 'value'),
         Input('tamanho-fralda-dropdown', 'value'),
         Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def atualizar_dados(beneficiado_selecionado, tamanho_fralda_selecionado, start_date, end_date):
        df = combinar_dados()

        print("Dados Beneficiado:")
        print(df.head())

        if df.empty:
            return [], [], {'data': [], 'layout': {'title': 'Distribuição de Fraldas por Tamanho'}}, {'data': [], 'layout': {'title': 'Distribuição de Beneficiados por Mês'}}, {'data': [], 'layout': {'title': 'Distribuição de Marcas de Fraldas'}}

        df_filtrado = df.copy()

        if beneficiado_selecionado and beneficiado_selecionado != 'all':
            df_filtrado = df_filtrado[df_filtrado['nome_beneficiado'] == beneficiado_selecionado]
        if tamanho_fralda_selecionado and tamanho_fralda_selecionado != 'all':
            df_filtrado = df_filtrado[df_filtrado['tamanho_liberado'] == tamanho_fralda_selecionado]
        if start_date and end_date:
            df_filtrado = df_filtrado[(pd.to_datetime(df_filtrado['data_inicio']) >= start_date) & (pd.to_datetime(df_filtrado['data_inicio']) <= end_date)]

        print("Dados Filtrados:")
        print(df_filtrado.head())

        # Quantidade de fraldas por beneficiado
        if 'marca_fralda' in df_filtrado.columns:
            quantidade_fraldas = df_filtrado.groupby(['nome_beneficiado', 'marca_fralda', 'data_inicio'])['quantidade_liberada'].sum().reset_index()
        else:
            quantidade_fraldas = df_filtrado.groupby(['nome_beneficiado', 'data_inicio'])['quantidade_liberada'].sum().reset_index()

        # Distribuição por tamanho de fralda
        tamanho_fralda = df_filtrado.groupby('tamanho_liberado')['quantidade_liberada'].sum().reset_index()

        # Distribuição por marca de fralda
        if 'marca_fralda' in df_filtrado.columns:
            marcas_fralda = df_filtrado.groupby('marca_fralda')['quantidade_liberada'].sum().reset_index()
        else:
            marcas_fralda = pd.DataFrame(columns=['marca_fralda', 'quantidade_liberada'])

        # Distribuição por mês e ano de início
        if 'data_inicio' in df_filtrado.columns:
            df_filtrado['mes_ano_inicio'] = pd.to_datetime(df_filtrado['data_inicio']).dt.to_period('M')
            beneficiados_mes = df_filtrado.groupby('mes_ano_inicio').size().reset_index(name='quantidade')
        else:
            beneficiados_mes = pd.DataFrame(columns=['mes_ano_inicio', 'quantidade'])

        # Dados para tabela de quantidade de fraldas
        columns_quantidade = [{"name": i, "id": i} for i in quantidade_fraldas.columns]
        data_quantidade = quantidade_fraldas.to_dict('records')

        # Gráfico de distribuição de fraldas por tamanho
        fig_tamanho_fralda = {
            'data': [
                go.Pie(
                    labels=tamanho_fralda['tamanho_liberado'],
                    values=tamanho_fralda['quantidade_liberada'],
                    name='Distribuição de Fraldas por Tamanho'
                )
            ],
            'layout': {
                'title': 'Distribuição de Fraldas por Tamanho'
            }
        }

        # Gráfico de distribuição de beneficiados por mês e ano
        fig_beneficiados_mes = {
            'data': [
                go.Bar(
                    x=beneficiados_mes['mes_ano_inicio'].astype(str),
                    y=beneficiados_mes['quantidade'],
                    name='Distribuição de Beneficiados por Mês e Ano'
                )
            ],
            'layout': {
                'title': 'Distribuição de Beneficiados por Mês e Ano'
            }
        }

        # Gráfico de distribuição de fraldas por marca
        fig_marcas_fralda = {
            'data': [
                go.Pie(
                    labels=marcas_fralda['marca_fralda'],
                    values=marcas_fralda['quantidade_liberada'],
                    name='Distribuição de Marcas de Fraldas'
                )
            ],
            'layout': {
                'title': 'Distribuição de Marcas de Fraldas'
            }
        }

        return data_quantidade, columns_quantidade, fig_tamanho_fralda, fig_beneficiados_mes, fig_marcas_fralda

    return app
