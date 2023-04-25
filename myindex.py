# bibliotecas e imports da pasta/bibliotecas
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from components import sidebar, extratos, dashboards

from globals import *

# Lista contendo links para os estilos utilizados na aplicação
estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
           "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.COSMO]

# URL do arquivo CSS da biblioteca dash_bootstrap_components
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"


# Cria uma instância do objeto Dash, passando o nome da aplicação e a lista de estilos como argumentos
app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])


# Define uma configuração para suprimir exceções em caso de callbacks faltantes
app.config['suppress_callback_exceptions'] = True

# Define uma configuração para servir scripts localmente
app.scripts.config.serve_locally = True

# Cria uma instância do servidor Flask que será usada pelo Dash
server = app.server

# DataFrames and Dcc.Store
df_receitas = pd.read_csv("df_receitas.csv", index_col=0, parse_dates=True)
df_receitas_aux = df_receitas.to_dict()

df_despesas = pd.read_csv("df_despesas.csv", index_col=0, parse_dates=True)
df_despesas_aux = df_despesas.to_dict()

list_receitas = pd.read_csv('df_cat_receita.csv', index_col=0)
list_receitas_aux = list_receitas.to_dict()

list_despesas = pd.read_csv('df_cat_despesa.csv', index_col=0)
list_despesas_aux = list_despesas.to_dict()


# =========  Layout  =========== #
content = html.Div(id="page-content")


app.layout = dbc.Container(children=[
    # criação de caixinhas de memória para manipular os dados do dataframe
    dcc.Store(id='store-receitas', data=df_receitas_aux),
    dcc.Store(id="store-despesas", data=df_despesas_aux),
    dcc.Store(id='stored-cat-receitas', data=list_receitas_aux),
    dcc.Store(id='stored-cat-despesas', data=list_despesas_aux),

    dbc.Row([
        dbc.Col([
            dcc.Location(id='url'),
            sidebar.layout
        ], md=2),
        dbc.Col([
            content
        ], md=10)
    ])
], fluid=True,)


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def render_page(pathname):
    if pathname == '/' or pathname == '/dashboards':
        return dashboards.layout
    if pathname == '/extratos':
        return extratos.layout


if __name__ == '__main__':
    app.run_server(debug=True)
