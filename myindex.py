# bibliotecas e imports da pasta/bibliotecas
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *

from components import expenses, revenues, sidebar, dashboards

from globals import *


# DataFrames and Dcc.Store
df_revenues = pd.read_csv(os.path.join(
    path_data_files, data_files['revenues']), index_col=0, parse_dates=True)
df_revenues_aux = df_revenues.to_dict()

df_expenses = pd.read_csv(os.path.join(
    path_data_files, data_files['expenses']), index_col=0, parse_dates=True)
df_expenses_aux = df_expenses.to_dict()

list_revenues = pd.read_csv(os.path.join(
    path_data_files, data_files['categories_revenues']), index_col=0)
list_revenues_aux = list_revenues.to_dict()

list_expenses = pd.read_csv(os.path.join(
    path_data_files, data_files['categories_expenses']), index_col=0)
list_expenses_aux = list_expenses.to_dict()


# =========  Layout  =========== #
content = html.Div(id="page-content")


app.layout = dbc.Container(children=[
    # criação de caixinhas de memória para manipular os dados do dataframe
    dcc.Store(id='store-revenues', data=df_revenues_aux),
    dcc.Store(id="store-expenses", data=df_expenses_aux),
    dcc.Store(id='stored-cat-revenues', data=list_revenues_aux),
    dcc.Store(id='stored-cat-expenses', data=list_expenses_aux),

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
    if pathname == '/analisar-expenses':
        return expenses.layout
    if pathname == '/analisar-revenues':
        return revenues.layout


if __name__ == '__main__':
    app.run_server(debug=True, port=8090)
