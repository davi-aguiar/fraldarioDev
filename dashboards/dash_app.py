import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
import pandas as pd
from flask import Flask, jsonify
import plotly.express as px
import random

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

API_KEY = 'AIzaSyAx4ZG02lnx0CYmh4h1wbKPN9rJjq2kn-4'

def geocode_address(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {
        'address': address,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

def get_farmacia_coordinates(farmacias):
    coordinates = []
    for farmacia in farmacias:
        if farmacia['bairro'] and farmacia['cidade'] and farmacia['estado'] and farmacia['cep']:
            address = f"{farmacia['bairro']}, {farmacia['cidade']} - {farmacia['estado']}, {farmacia['cep']}"
            lat, lng = geocode_address(address)
            if lat and lng:
                coordinates.append({'latitude': lat, 'longitude': lng, 'name': farmacia['nomeFantasia'], 'quantidade': farmacia['total_fraldas_entregues']})
            else:
                print(f"Falha ao geocodificar o endereço: {address}")
        else:
            print(f"Informações insuficientes para geocodificação: {farmacia}")
    print(f"Coordenadas das farmácias: {coordinates}")
    return coordinates

def create_map(coordinates, mode='normal'):
    if not coordinates:
        print("Nenhuma coordenada encontrada para criar o mapa.")
        return go.Figure()
    
    df = pd.DataFrame(coordinates)
    
    if mode == 'normal':
        fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', size='quantidade', hover_name='name',
                                hover_data={'latitude': False, 'longitude': False},
                                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
    elif mode == 'heatmap':
        fig = px.density_mapbox(df, lat='latitude', lon='longitude', z='quantidade', radius=10,
                                center=dict(lat=df['latitude'].mean(), lon=df['longitude'].mean()), zoom=10,
                                mapbox_style="open-street-map", color_continuous_scale=px.colors.cyclical.IceFire)
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def load_dados_farmacia():
        try:
            response = requests.get('http://127.0.0.1:5000/dados_farmacia')
            response.raise_for_status()
            data = response.json()
            print(f"Dados das farmácias carregados: {data}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Erro ao carregar dados das farmácias: {e}")
            return []
        except ValueError as e:
            print(f"Erro ao converter dados para JSON: {e}")
            return []

def create_dash_app(server):
    app = dash.Dash(__name__, server=server, url_base_pathname='/dash/')

    app.title = "Dashboard de Entrega de Fraldas"

    def load_dados_antigos():
        try:
            response = requests.get('http://127.0.0.1:5000/dados_antigos')
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Erro ao carregar dados antigos: {e}")
            return []
        except ValueError as e:
            print(f"Erro ao converter dados para JSON: {e}")
            return []

    def load_dados_transacao():
        try:
            response = requests.get('http://127.0.0.1:5000/dados_transacao')
            response.raise_for_status()
            data = response.json()
            print(f"Dados de transações carregados: {data}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Erro ao carregar dados das transações: {e}")
            return []
        except ValueError as e:
            print(f"Erro ao converter dados para JSON: {e}")
            return []

    app.layout = html.Div(className='dashboard-container', children=[
        html.H1(children='Dashboard de Entrega de Fraldas'),

        html.Div(id='texto'),

        html.Div(children=[
            dcc.Dropdown(
                id='farmacia-dropdown',
                placeholder="Selecione uma farmácia",
                className='dcc-dropdown'
            ),
            dcc.Dropdown(
                id='mes-dropdown',
                placeholder="Selecione um mês",
                className='dcc-dropdown'
            ),
            dcc.Dropdown(
                id='dia-dropdown',
                placeholder="Selecione um dia",
                className='dcc-dropdown'
            ),
        ], className='filter-container'),

        html.Div(children=[
            html.Button('Alternar Modo do Mapa', id='toggle-map-mode', n_clicks=0),
        ], style={'padding': '20px'}),

        html.Div(children=[
            html.Div(children=[
                html.H3("Quantidade Total por Farmácia"),
                dash_table.DataTable(
                    id='tabela-dados-antigos',
                    columns=[],
                    data=[],
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'height': 'auto',
                        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                        'whiteSpace': 'normal',
                        'fontFamily': 'Poppins, sans-serif'
                    },
                )
            ], style={'width': '48%', 'display': 'inline-block', 'fontFamily': 'Poppins, sans-serif'}),

            html.Div(children=[
                html.H3("Quantidade Diária Retirada"),
                dash_table.DataTable(
                    id='tabela-dados-transacao',
                    columns=[],
                    data=[],
                    page_size=10,
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'height': 'auto',
                        'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                        'whiteSpace': 'normal',
                        'fontFamily': 'Poppins, sans-serif'
                    },
                )
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right','fontFamily': 'Poppins, sans-serif'})
        ]),

        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id='grafico-fraldas', className='dcc-graph')
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div(children=[
                dcc.Graph(id='grafico-pizza', className='dcc-graph')
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ]),

        html.Div(children=[
            dcc.Graph(id='grafico-fraldas-dia', className='dcc-graph')
        ]),

        html.Div(children=[
            html.Div(children=[
                dcc.Graph(id='grafico-marca', className='dcc-graph')
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div(children=[
                dcc.Graph(id='grafico-media-marca', className='dcc-graph')
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
        ]),

        html.Div(children=[
            dcc.Graph(id='mapa-farmacias', className='dcc-graph')
        ])
    ])

    @app.callback(
        [Output('farmacia-dropdown', 'options'),
         Output('mes-dropdown', 'options'),
         Output('dia-dropdown', 'options')],
        [Input('farmacia-dropdown', 'value')]
    )
    def update_dropdown_options(_):
        dados_antigos = load_dados_antigos()
        dados_transacao = load_dados_transacao()
        dados = dados_antigos + dados_transacao

        if not isinstance(dados, list):
            print(f"Dados inválidos: {dados}")
            return [{'label': 'Erro ao carregar dados', 'value': 'error'}], [{'label': 'Erro ao carregar dados', 'value': 'error'}], [{'label': 'Erro ao carregar dados', 'value': 'error'}]

        df = pd.DataFrame(dados)
        print(f"Colunas do DataFrame: {df.columns}")

        if 'data' in df.columns:
            df['mes'] = pd.to_datetime(df['data'], errors='coerce').dt.to_period('M').astype(str)
            df['dia'] = pd.to_datetime(df['data'], errors='coerce').dt.day

        opcoes_farmacias = [{'label': 'Todas as Farmácias', 'value': 'all'}] + [{'label': farmacia, 'value': farmacia} for farmacia in df['farmacia'].unique()]
        opcoes_meses = [{'label': 'Todos os Meses', 'value': 'all'}] + [{'label': mes, 'value': mes} for mes in df['mes'].unique()] if 'mes' in df.columns else []
        opcoes_dias = [{'label': 'Todos os Dias', 'value': 'all'}] + [{'label': str(dia), 'value': str(dia)} for dia in df['dia'].unique()] if 'dia' in df.columns else []

        return opcoes_farmacias, opcoes_meses, opcoes_dias

    @app.callback(
        [Output('grafico-fraldas', 'figure'),
         Output('grafico-pizza', 'figure'),
         Output('grafico-fraldas-dia', 'figure'),
         Output('grafico-marca', 'figure'),
         Output('grafico-media-marca', 'figure'),
         Output('mapa-farmacias', 'figure'),
         Output('texto', 'children'),
         Output('tabela-dados-antigos', 'data'),
         Output('tabela-dados-antigos', 'columns'),
         Output('tabela-dados-transacao', 'data'),
         Output('tabela-dados-transacao', 'columns')],
        [Input('farmacia-dropdown', 'value'), Input('mes-dropdown', 'value'), Input('dia-dropdown', 'value'), Input('toggle-map-mode', 'n_clicks')]
    )
    def atualizar_graficos(farmacia_selecionada, mes_selecionado, dia_selecionado, n_clicks):
        dados_antigos = load_dados_antigos()
        dados_transacao = load_dados_transacao()
        dados_farmacia = load_dados_farmacia()

        df_antigos = pd.DataFrame(dados_antigos)
        df_transacao = pd.DataFrame(dados_transacao)

        if 'data' in df_transacao.columns:
            df_transacao['mes'] = pd.to_datetime(df_transacao['data'], errors='coerce').dt.to_period('M').astype(str)
            df_transacao['dia'] = pd.to_datetime(df_transacao['data'], errors='coerce').dt.day.astype(int)

        print("Dados transação antes do filtro:")
        print(df_transacao)

        df_filtrado_antigos = df_antigos.copy()
        df_filtrado_transacao = df_transacao.copy()

        if farmacia_selecionada and farmacia_selecionada != 'all':
            df_filtrado_antigos = df_filtrado_antigos[df_filtrado_antigos['farmacia'] == farmacia_selecionada]
            df_filtrado_transacao = df_filtrado_transacao[df_filtrado_transacao['farmacia'] == farmacia_selecionada]
        if mes_selecionado and mes_selecionado != 'all' and 'mes' in df_filtrado_transacao.columns:
            df_filtrado_transacao = df_filtrado_transacao[df_filtrado_transacao['mes'] == mes_selecionado]
        if dia_selecionado and dia_selecionado != 'all' and 'dia' in df_filtrado_transacao.columns:
            try:
                dia_selecionado = int(dia_selecionado)
                df_filtrado_transacao = df_filtrado_transacao[df_filtrado_transacao['dia'] == dia_selecionado]
            except ValueError:
                print(f"Valor inválido para dia_selecionado: {dia_selecionado}")

        print("Dados transação após o filtro:")
        print(df_filtrado_transacao)

        # Verificar as colunas disponíveis nos DataFrames
        print(f"Colunas em df_antigos: {df_antigos.columns}")
        print(f"Colunas em df_transacao: {df_transacao.columns}")

        # Removendo as colunas desnecessárias
        df_filtrado_transacao = df_filtrado_transacao.drop(columns=['media marca mais retirada', 'media tamanho mais retirado'], errors='ignore')

        columns_antigos = [{"name": i, "id": i} for i in df_filtrado_antigos.columns]
        data_antigos = df_filtrado_antigos.to_dict('records')

        columns_transacao = [{"name": i, "id": i} for i in df_filtrado_transacao.columns]
        data_transacao = df_filtrado_transacao.to_dict('records')

        fig_barras = {
            'data': [
                go.Bar(
                    x=df_filtrado_transacao['farmacia'],
                    y=df_filtrado_transacao['quantidade'],
                    name='Fraldas Entregues Diariamente'
                )
            ],
            'layout': {
                'title': 'Quantidade de Fraldas Entregues Diariamente'
            }
        }

        if 'mes' in df_filtrado_transacao.columns and not df_filtrado_transacao.empty:
            df_agrupado_mes = df_filtrado_transacao.groupby('mes')['quantidade'].sum()
            fig_pizza = {
                'data': [
                    go.Pie(
                        labels=df_agrupado_mes.index,
                        values=df_agrupado_mes.values,
                        name='Proporção de Fraldas Entregues por Mês'
                    )
                ],
                'layout': {
                    'title': 'Proporção de Fraldas Entregues por Mês'
                }
            }
        else:
            fig_pizza = {
                'data': [],
                'layout': {
                    'title': 'Proporção de Fraldas Entregues por Mês (dados não disponíveis)'
                }
            }

        fig_dia = {
            'data': [
                go.Scatter(
                    x=df_filtrado_transacao['dia'],
                    y=df_filtrado_transacao['quantidade'],
                    mode='lines+markers',
                    name='Fraldas Entregues por Dia'
                )
            ],
            'layout': {
                'title': 'Quantidade de Fraldas Entregues por Dia'
            }
        }

        # Gráfico de Marcas mais Retiradas
        if 'marca' in df_filtrado_transacao.columns and not df_filtrado_transacao.empty:
            df_agrupado_marca = df_filtrado_transacao.groupby('marca')['quantidade'].sum()
            fig_marca = {
                'data': [
                    go.Bar(
                        x=df_agrupado_marca.index,
                        y=df_agrupado_marca.values,
                        name='Quantidade por Marca'
                    )
                ],
                'layout': {
                    'title': 'Quantidade de Fraldas por Marca'
                }
            }
        else:
            fig_marca = {
                'data': [],
                'layout': {
                    'title': 'Quantidade de Fraldas por Marca (dados não disponíveis)'
                }
            }

        # Gráfico da Média da Marca mais Retirada
        if 'marca' in df_transacao.columns and not df_transacao.empty:
            media_marca = df_transacao.groupby('marca')['quantidade'].mean().sort_values(ascending=False)
            fig_media_marca = {
                'data': [
                    go.Bar(
                        x=media_marca.index,
                        y=media_marca.values,
                        name='Média de Fraldas por Marca'
                    )
                ],
                'layout': {
                    'title': 'Média de Fraldas por Marca'
                }
            }
        else:
            fig_media_marca = {
                'data': [],
                'layout': {
                    'title': 'Média de Fraldas por Marca (dados não disponíveis)'
                }
            }

        # Alternar entre modos de mapa
        mode = 'heatmap' if n_clicks % 2 == 1 else 'normal'
        
        coordinates = get_farmacia_coordinates(dados_farmacia)
        fig_map = create_map(coordinates, mode=mode)

        if farmacia_selecionada == 'all' and mes_selecionado == 'all' and dia_selecionado == 'all':
            texto = 'Você selecionou todas as farmácias, todos os meses e todos os dias'
        elif farmacia_selecionada == 'all' and dia_selecionado == 'all':
            texto = f'Você selecionou todas as farmácias no mês {mes_selecionado}'
        elif mes_selecionado == 'all' and dia_selecionado == 'all':
            texto = f'Você selecionou a farmácia {farmacia_selecionada} em todos os meses'
        elif farmacia_selecionada == 'all':
            texto = f'Você selecionou todas as farmácias no mês {mes_selecionado} e no dia {dia_selecionado}'
        elif mes_selecionado == 'all':
            texto = f'Você selecionou a farmácia {farmacia_selecionada} em todos os meses e no dia {dia_selecionado}'
        elif dia_selecionado == 'all':
            texto = f'Você selecionou a farmácia {farmacia_selecionada} no mês {mes_selecionado}'
        else:
            texto = f'Você selecionou a farmácia {farmacia_selecionada} no mês {mes_selecionado} e no dia {dia_selecionado}'

        return (fig_barras, fig_pizza, fig_dia, fig_marca, 
                fig_media_marca, fig_map, 
                texto, data_antigos, columns_antigos, data_transacao, columns_transacao)

    return app

if __name__ == '__main__':
    server = Flask(__name__)
    app = create_dash_app(server)
    server.run(debug=True)
