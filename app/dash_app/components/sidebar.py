from ..data_loader import *
import pandas as pd
from app import app
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html, dcc, dash_table, callback_context
import dash
import os

## Services ##
from ...utils import StatemantTransform
from .modals import *


# ========= Layout ========= #
layout = dbc.Col([
    html.Div([
        html.H1("Personal Budget",
                className="display-5 text-primary fw-bolder mt-3"),
        html.P("By Vitor Rocha", className="text-muted fs-6"),
        html.Hr(className="my-3")
    ], style={"text-align": "center"}),

    # seção de lançamento de receita e despesa----------------------------------
    dbc.Row([
        dbc.Col([
            dbc.Button(color='success', id='new-receita',
                       children=['+ Receita'])
        ], width=6),
        dbc.Col([
            dbc.Button(color='danger', id='new-despesa',
                       children=['- Despesa'])
        ], width=6)
    ], style={'text-align': 'center'}),
    # bot]ao de importar csv
    dbc.Row([
        dbc.Col([
            dbc.Button(color='primary', id='open_modal_button',
                       children=['Importar Extrato'])
        ], width=12)
    ], style={'text-align': 'center'}, className='mt-3'),

    ### Modal importar extrato ###
    modal_import_statement(
        'modal_import_statement_id', 
        'Importar CSV', 
        'Adicionar transações'
    ),
    
    ### Modal receita ###
    modal_add_transaction('receita', 'Receita', cat_receita),   
    
    ### Modal despesa ###
    modal_add_transaction('despesa', 'Despesa', cat_despesa),

    # seção de navegação--------------------
    html.Hr(),
    dcc.Location(id='url', refresh=False),
    dbc.Nav([
        dbc.NavItem(dbc.NavLink(
            "Dashboard", href="/dashboards", active="exact", id="dashboard-link")),
        dbc.NavItem([
            dbc.NavLink("Extratos", id="extratos-toggle", active="exact")], id="extratos-link"),
        dbc.Collapse([
            dbc.NavLink("Analisar Despesas",
                        href="/analisar-despesas", active="exact", style={"marginLeft": "20px", "fontSize": "0.9em"}, id="despesas-link"),
            dbc.NavLink("Analisar Receitas",
                        href="/analisar-receitas", active="exact", style={"marginLeft": "20px", "fontSize": "0.9em"}, id="receitas-link"),
        ], id="extratos-collapse", is_open=False),
    ], vertical=True, id='nav-buttons', style={'margin-bottom': '50px'})

], id='sidebar_inteira')


# =========  Callbacks  =========== #

# # Toggle extratos menu collapse com o mouse hover
@app.callback(
    Output("extratos-collapse", "is_open"),
    [Input("extratos-toggle", "n_clicks"),
     Input('url', 'pathname')],  # Nova entrada
    [State("extratos-collapse", "is_open")],
)
def toggle_collapse(n, pathname, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = 'No clicks yet'
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == "extratos-toggle":
        return not is_open
    elif trigger_id == 'url':
        if pathname == "/analisar-despesas" or pathname == "/analisar-receitas":
            return True
        elif pathname == "/dashboards":
            return False
    return is_open


# pintar o menu de acordo com a página atual
@app.callback(
    [Output("extratos-toggle", "className"),
     Output("dashboard-link", "className"),
     Output("despesas-link", "className"),
     Output("receitas-link", "className")],
    [Input('url', 'pathname')]
)
def update_class(pathname):
    extratos_class = ""
    dashboard_class = ""
    despesas_class = ""
    receitas_class = ""

    if pathname == "/dashboards" or pathname == "/":
        dashboard_class = "active-singlelink"
    elif pathname == "/analisar-despesas":
        extratos_class = "active-grouplink"
        despesas_class = "active-sublink"
    elif pathname == "/analisar-receitas":
        extratos_class = "active-grouplink"
        receitas_class = "active-sublink"

    return extratos_class, dashboard_class, despesas_class, receitas_class

# # open/close modal importar csv
callback_open_modal("open_modal_button", "modal_import_statement_id")
# open/close modal receita/despesa
callback_open_modal("new-receita", "modal-new-receita")
callback_open_modal("new-despesa", "modal-new-despesa")


# gerenciar adicionar receitas e despesas
calback_add_transactions(
    'add-statement', 
    'salvar_receita', 
    'salvar_despesa', 
    'temporary-contents-statement', 
    'txt-receita', 
    'valor_receita', 
    'date-receita', 
    'switches-input-receita', 
    'select_receita', 
    'txt-despesa', 
    'valor_despesa', 
    'date-despesa', 
    'switches-input-despesa', 
    'select_despesa', 
    'store-receitas', 
    'store-despesas'
    )


## Add/Remove categoria receita/despesa
callback_manege_category_modal('receita')
callback_manege_category_modal('despesa')


## callback para se caso o dcc.Store estiver preenchido, aparece uma tabela com as transações
banks_options = [
    {"label": "Wise", "value": "Wise"},
    {"label": "CGD", "value": "CGD"},
    {"label": "Nubank", "value": "Nubank"},
    {"label": "Inter", "value": "Inter"}
]

callback_manage_div_upload_data(
    'div-data-import-statement', 
    'modal_import_statement_id', 
    'temporary-contents-statement',
    banks_options
    )
    
## Importação de extratos bancários e limpar store caso o modal seja fechado ou importado
callback_statement_store(
    'temporary-contents-statement', 
    'modal_import_statement_id', 
    'add-statement',
    'upload-data-import-statement', 
    'select-banco')
