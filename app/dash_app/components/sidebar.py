from ..data_loader import *
from ...app import app
import pandas as pd
from app import app
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html, dcc, callback_context
import dash
import os

## Services ##
from ...utils import StatemantTransform
from .modals import modal_add_transaction, callback_manege_category_modal, callback_open_modal


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
            dbc.Button(color='primary', id='import-button',
                       children=['Importar Extrato'])
        ], width=12)
    ], style={'text-align': 'center'}, className='mt-3'),

    ### Modal importar extrato ###

    dbc.Modal(
        [
            dbc.ModalHeader("Importar CSV"),
            dbc.ModalBody(
                [
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Selecione o banco:"),
                            dbc.Select(
                                id="select-banco",
                                options=[
                                    {"label": "Wise", "value": "Wise"},
                                    {"label": "OutroBanco", "value": "OutroBanco"},
                                ],
                                value="Wise",
                            ),
                        ]),
                    ], class_name="mb-3"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Arraste e solte ou ',
                            html.A('Selecione do seu computador', className="text-primary", style={
                                   "text-decoration": "none", "cursor": "pointer", "font-weight": "bold"})
                        ]),
                        style={
                            'width': '100',
                            'height': '4rem',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '4%',
                            'textAlign': 'center',
                        },
                        multiple=False
                    ),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Fechar", id="close-button", className="ml-auto")
            ),
        ],
        id="import-modal",
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

# # Pop-up importar csv


@app.callback(
    Output("import-modal", "is_open"),
    [Input("import-button", "n_clicks"), Input("close-button", "n_clicks")],
    [State("import-modal", "is_open")],
)
def toggle_modal_import(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# open/close modal receita/despesa
callback_open_modal('receita')
callback_open_modal('despesa')


# gerenciar adicionar receitas e despesas
@app.callback(
    [
        Output('store-receitas', 'data'),
        Output('store-despesas', 'data')],
    [
        Input('upload-data', 'contents'),
        Input('salvar_receita', 'n_clicks'),
        Input('salvar_despesa', 'n_clicks')],
    [
        State('upload-data', 'filename'),
        State('txt-receita', 'value'),
        State('valor_receita', 'value'),
        State('date-receita', 'date'),
        State('switches-input-receita', 'value'),
        State('select_receita', 'value'),
        State('txt-despesa', 'value'),
        State('valor_despesa', 'value'),
        State('date-despesa', 'date'),
        State('switches-input-despesa', 'value'),
        State('select_despesa', 'value'),
        State('store-receitas', 'data'),
        State('store-despesas', 'data'),
        State('select-banco', 'value'),
    ]
)
def combined_callback(contents, n_clicks_receita, n_clicks_despesa, filename, descricao_receita, valor_receita, date_receita, switches_receita, categoria_receita, descricao_despesa, valor_despesa, date_despesa, switches_despesa, categoria_despesa, dict_receitas, dict_despesas, selected_banco):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'upload-data':
        if selected_banco == "Wise":
            extrato = StatemantTransform(contents)
            receitas_transformed, despesas_transformed = extrato.transform_wise()

            df_receitas_novo = pd.concat([df_receitas, receitas_transformed])
            df_despesas_novo = pd.concat([df_despesas, despesas_transformed])

            df_receitas_novo.to_csv(os.path.join(
                data_dir, data_files['receitas']))
            df_despesas_novo.to_csv(os.path.join(
                data_dir, data_files['despesas']))

        return df_receitas_novo.to_dict(), df_despesas_novo.to_dict()

    elif triggered_id == 'salvar_receita':
        if n_clicks_receita and not (valor_receita == "" or valor_receita is None):
            valor_receita = round(float(valor_receita), 2)
            date_receita = pd.to_datetime(date_receita).date()
            categoria_receita = categoria_receita[0] if type(
                categoria_receita) == list else categoria_receita

            recebido = 1 if 1 in switches_receita else 0
            fixo = 1 if 2 in switches_receita else 0

            df_receitas.loc[df_receitas.shape[0]] = [
                valor_receita, recebido, fixo, date_receita, categoria_receita, descricao_receita]
            df_receitas.to_csv(os.path.join(
                data_dir, data_files['receitas']))

            data_return = df_receitas.to_dict()
            return data_return, dash.no_update

    elif triggered_id == 'salvar_despesa':
        if n_clicks_despesa and not (valor_despesa == "" or valor_despesa is None):
            valor_despesa = round(float(valor_despesa), 2)
            date_despesa = pd.to_datetime(date_despesa).date()
            categoria_despesa = categoria_despesa[0] if type(
                categoria_despesa) == list else categoria_despesa

            recebido = 1 if 1 in switches_despesa else 0
            fixo = 1 if 2 in switches_despesa else 0

            df_despesas.loc[df_despesas.shape[0]] = [
                valor_despesa, recebido, fixo, date_despesa, categoria_despesa, descricao_despesa]
            df_despesas.to_csv(os.path.join(
                data_dir, data_files['despesas']))

            data_return = df_despesas.to_dict()

        return dash.no_update, df_despesas.to_dict()

    return dash.no_update, dash.no_update

## Add/Remove categoria receita/despesa
callback_manege_category_modal('receita')
callback_manege_category_modal('despesa')
