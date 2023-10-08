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
                    html.Div(id='div-data-import-statement', children=[
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
                            id='upload-data-import-statement',
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
                        )
                    ]
                             ),
                    dcc.Store(id='temporary-contents-statement', storage_type='memory'),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Adicionar transações", id="add-statement", className="ml-auto")
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

# # open/close modal importar csv
callback_open_modal("import-button", "import-modal")
# open/close modal receita/despesa
callback_open_modal("new-receita", "modal-new-receita")
callback_open_modal("new-despesa", "modal-new-despesa")


# gerenciar adicionar receitas e despesas
@app.callback(
    [
        Output('store-receitas', 'data'),
        Output('store-despesas', 'data')],
    [
        Input('add-statement', 'n_clicks'),
        Input('salvar_receita', 'n_clicks'),
        Input('salvar_despesa', 'n_clicks')],
    [
        State('temporary-contents-statement', 'data'),
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
    ]
)
def manage_add_transactions_callback(n_clicks_add_statemant, n_clicks_receita, n_clicks_despesa, contents, descricao_receita, valor_receita, date_receita, switches_receita, categoria_receita, descricao_despesa, valor_despesa, date_despesa, switches_despesa, categoria_despesa, dict_receitas, dict_despesas):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    df_receitas = pd.DataFrame(dict_receitas)
    df_despesas = pd.DataFrame(dict_despesas)

    if triggered_id == 'add-statement' and contents != {} and n_clicks_add_statemant is not None:
        receitas_transformed = pd.DataFrame(contents['receitas'])
        despesas_transformed = pd.DataFrame(contents['despesas'])

        df_receitas_novo = pd.concat([df_receitas, receitas_transformed])
        df_despesas_novo = pd.concat([df_despesas, despesas_transformed])

        df_receitas_novo.to_csv(os.path.join(
            data_dir, data_files['receitas']))
        df_despesas_novo.to_csv(os.path.join(
            data_dir, data_files['despesas']))
        return df_receitas_novo.to_dict(), df_despesas_novo.to_dict()

    elif triggered_id == 'salvar_receita' and n_clicks_receita is not None:
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

    elif triggered_id == 'salvar_despesa' and n_clicks_despesa is not None:
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


## callback para se caso o dcc.Store estiver preenchido, aparece uma tabela com as transações
@app.callback(
    Output('div-data-import-statement', 'children'),
    Output('import-modal', 'size'),
    Input('temporary-contents-statement', 'data')
)
def div_upload_data(data):
    if data:
        df_receitas_imported = pd.DataFrame(data['receitas'])
        df_receitas_imported['Tipo'] = 'Receita'
        df_despesas_imported = pd.DataFrame(data['despesas'])
        df_despesas_imported['Tipo'] = 'Despesa'
        df_combined = pd.concat([df_receitas_imported, df_despesas_imported])
        df_combined.fillna('-', inplace=True)     
        df_combined['Valor'] = df_combined['Valor'].apply(lambda x: f'$ {x:.2f}'.replace('.', ','))
        df_combined.loc[df_combined['Efetuado'] == 0, 'Efetuado'] = 'Não'
        df_combined.loc[df_combined['Efetuado'] == 1, 'Efetuado'] = 'Sim'
        df_combined.loc[df_combined['Fixo'] == 0, 'Fixo'] = 'Não'
        df_combined.loc[df_combined['Fixo'] == 1, 'Fixo'] = 'Sim'
        df_combined['Data'] = pd.to_datetime(df_combined['Data']).dt.date
        df_combined.sort_values(by='Data', ascending=False, inplace=True)
        cols = df_combined.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df_combined = df_combined[cols]
        
        table = dash_table.DataTable(
            id='table-data-import-statement',
            columns=[{"name": i, "id": i} for i in df_combined.columns],
            data=df_combined.to_dict('records'),
            page_action="native",
            page_current=0,
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
                {
                    'if': {'column_id': 'Efetuado',
                        'filter_query': '{Efetuado} eq "Não"'},
                    'backgroundColor': 'tomato',
                    'color': 'white'
                },
                {
                    'if': {'column_id': 'Efetuado',
                        'filter_query': '{Efetuado} eq "Sim"'},
                    'color': 'limegreen'
                },
                {
                    ## coluna Tipo Receita verde e Despesa vermelho
                    'if': {'column_id': 'Tipo',
                        'filter_query': '{Tipo} eq "Receita"'},
                    'color': 'limegreen'
                },
                {
                    'if': {'column_id': 'Tipo',
                        'filter_query': '{Tipo} eq "Despesa"'},
                    'color': 'tomato',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
        )
        return table, 'lg'
    else:
        return dash.no_update
    
## Importação de extratos bancários e limpar store caso o modal seja fechado
@app.callback(
    Output('temporary-contents-statement', 'data'),
    [
        Input('upload-data-import-statement', 'contents'),
        Input('import-modal', 'is_open')
    ],
    State('select-banco', 'value'),
)
def process_file(contents, modal_import_statement_is_open, banco):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == 'import-modal' and not modal_import_statement_is_open:
        return None
    elif triggered_id == 'upload-data-import-statement' and contents is not None:
        extrato = StatemantTransform(contents)
        if banco == 'Wise':
            receitas_transformed, despesas_transformed = extrato.transform_wise()
            return {'receitas': receitas_transformed.to_dict(), 'despesas': despesas_transformed.to_dict()}
    else:
        raise dash.exceptions.PreventUpdate