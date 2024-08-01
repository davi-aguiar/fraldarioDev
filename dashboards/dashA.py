import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import requests
import plotly.graph_objs as go

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

def create_dashboard_autorizador(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard_autorizador/')

    app.title = "Dashboard de Autorizadores"

    # Layout da aplicação
    app.layout = html.Div(className='dashboard-container', children=[
        html.H1(children='Dashboard de Autorizadores'),

        # Filtros
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dcc.Dropdown(
                    id='autorizador-dropdown',
                    placeholder="Selecione um autorizador",
                    className='dcc-dropdown'
                ),
            ])
        ]),

        # Tabela para mostrar quantidade de beneficiados por autorizador
        html.Div(className='row', children=[
            html.Div(className='twelve columns', children=[
                html.H3("Quantidade de Beneficiados Cadastrados por Autorizador"),
                dash_table.DataTable(
                    id='tabela-beneficiados',
                    columns=[],
                    data=[],
                    style_table={'overflowX': 'auto', 'fontFamily': 'Poppins, sans-serif'},
                    style_cell={
                        'height': 'auto',
                        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                        'whiteSpace': 'normal',
                        'fontFamily': 'Poppins, sans-serif'
                    },
                )
            ])
        ]),

        # Gráfico para mostrar quantidade de beneficiados por autorizador
        html.Div(className='row', children=[
            html.Div(className='twelve columns', children=[
                dcc.Graph(id='grafico-beneficiados')
            ])
        ])
    ])

    @app.callback(
        Output('autorizador-dropdown', 'options'),
        [Input('autorizador-dropdown', 'value')]
    )
    def update_dropdown_options(_):
        dados = load_dados_autorizador()
        if not dados:
            print("Nenhum dado de autorizador foi retornado.")
        else:
            print(f"Dados retornados de autorizador: {dados}")

        df = pd.DataFrame(dados)
        print(f"Colunas do DataFrame de Autorizadores: {df.columns}")

        opcoes_autorizadores = [{'label': 'Todos os Autorizadores', 'value': 'all'}] + [{'label': autorizador, 'value': autorizador} for autorizador in df['nomeAutorizador'].unique()]

        return opcoes_autorizadores

    @app.callback(
        [Output('tabela-beneficiados', 'data'),
         Output('tabela-beneficiados', 'columns'),
         Output('grafico-beneficiados', 'figure')],
        [Input('autorizador-dropdown', 'value')]
    )
    def atualizar_dados(autorizador_selecionado):
        dados_autorizador = load_dados_autorizador()
        dados_beneficiado = load_dados_beneficiado()

        if not dados_autorizador:
            print("Nenhum dado de autorizador foi retornado.")
        else:
            print(f"Dados retornados de autorizador: {dados_autorizador}")

        if not dados_beneficiado:
            print("Nenhum dado de beneficiado foi retornado.")
        else:
            print(f"Dados retornados de beneficiado: {dados_beneficiado}")

        df_autorizador = pd.DataFrame(dados_autorizador)
        df_beneficiado = pd.DataFrame(dados_beneficiado)

        # Garantir que os tipos dos IDs são os mesmos para a junção
        df_autorizador['id_usuario'] = df_autorizador['id_usuario'].astype(int)
        df_beneficiado['id_autorizador'] = df_beneficiado['id_autorizador'].astype(int)

        print("Dados Autorizador:")
        print(df_autorizador.head())
        print("Dados Beneficiado:")
        print(df_beneficiado.head())

        if df_beneficiado.empty:
            return [], [], {'data': [], 'layout': {'title': 'Beneficiados por Autorizador'}}

        df_filtrado = df_beneficiado.copy()

        if autorizador_selecionado and autorizador_selecionado != 'all':
            autorizador_ids = df_autorizador[df_autorizador['nomeAutorizador'] == autorizador_selecionado]['id_usuario']
            print(f"IDs de autorizadores selecionados: {autorizador_ids.tolist()}")
            df_filtrado = df_filtrado[df_filtrado['id_autorizador'].isin(autorizador_ids)]
            print("Dados Filtrados por autorizador:")
            print(df_filtrado.head())

        if df_filtrado.empty:
            print("Dados Filtrados estão vazios após aplicar os filtros.")
            return [], [], {'data': [], 'layout': {'title': 'Beneficiados por Autorizador'}}

        # Quantidade de beneficiados cadastrados por autorizador
        quantidade_beneficiados = df_filtrado.groupby('id_autorizador').size().reset_index(name='quantidade_beneficiados')
        quantidade_beneficiados = quantidade_beneficiados.merge(df_autorizador[['id_usuario', 'nomeAutorizador']], left_on='id_autorizador', right_on='id_usuario', how='left')
        quantidade_beneficiados = quantidade_beneficiados[['nomeAutorizador', 'quantidade_beneficiados']]

        print("Quantidade de Beneficiados:")
        print(quantidade_beneficiados.head())

        # Dados para tabela de beneficiados por autorizador
        columns_beneficiados = [{"name": i, "id": i} for i in quantidade_beneficiados.columns]
        data_beneficiados = quantidade_beneficiados.to_dict('records')

        # Gráfico de beneficiados por autorizador
        fig = go.Figure(data=[
            go.Bar(
                x=quantidade_beneficiados['nomeAutorizador'],
                y=quantidade_beneficiados['quantidade_beneficiados']
            )
        ])
        fig.update_layout(title='Beneficiados por Autorizador',
                          xaxis_title='Autorizador',
                          yaxis_title='Quantidade de Beneficiados')

        return data_beneficiados, columns_beneficiados, fig

    return app
