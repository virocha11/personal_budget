from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import app
from components import despesas, sidebar, dashboards, receitas

from data_loader import *


df_receitas = pd.read_csv(os.path.join(
    data_dir, data_files['receitas']), index_col=0, parse_dates=True)
df_receitas_aux = df_receitas.to_dict()

df_despesas = pd.read_csv(os.path.join(
    data_dir, data_files['despesas']), index_col=0, parse_dates=True)
df_despesas_aux = df_despesas.to_dict()

list_receitas = pd.read_csv(os.path.join(
    data_dir, data_files['categorias_receitas']), index_col=0)
list_receitas_aux = list_receitas.to_dict()

list_despesas = pd.read_csv(os.path.join(
    data_dir, data_files['categorias_despesas']), index_col=0)
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
            dcc.Location(id='url_index'),
            sidebar.layout
        ], md=2, className="sticky-sidebar"),
        dbc.Col([
            content
        ], md=10, className='px-2')
    ])
], fluid=True,)


@app.callback(Output('page-content', 'children'), [Input('url_index', 'pathname')])
def render_page(pathname):
    if pathname == '/' or pathname == '/dashboards':
        return dashboards.layout
    if pathname == '/analisar-despesas':
        return despesas.layout
    if pathname == '/analisar-receitas':
        return receitas.layout

if __name__ == '__main__':
    app.run_server(debug=True)