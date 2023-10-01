from globals import *
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, date
from app import app
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash
import os
import base64 as b64
import io
# ========= Layout ========= #
layout = dbc.Col([
    html.Div([
        html.H1("Personal Budget", className="display-5 text-primary fw-bolder mt-3"),
        html.P("By Vitor Rocha", className="text-muted fs-6"),
        html.Hr(className="my-3")
    ], style={"text-align": "center"}),

    # seção de lançamento de revenue e expense----------------------------------
    dbc.Row([
        dbc.Col([
            dbc.Button(color='success', id='new-revenue',
                       children=['+ Revenue'])
        ], width=6),
        dbc.Col([
            dbc.Button(color='danger', id='new-expense',
                       children=['- Expense'])
        ], width=6)
    ], style={'text-align': 'center'}),
    # bot]ao de importar csv
    dbc.Row([
        dbc.Col([
            dbc.Button(color='primary', id='import-button',
                       children=['Import bank statement'])
        ], width=12)
    ], style={'text-align': 'center'}, className='mt-3'),

    dbc.Modal(
        [
            dbc.ModalHeader("Import CSV Statement"),
            dbc.ModalBody(
                dcc.Upload(
                    id='upload-data',
                    children=html.Button('Selecione o arquivo CSV'),
                    multiple=False
                )
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-button", className="ml-auto")
            ),
        ],
        id="import-modal",
    ),
    ### Modal revenue ###
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Add Receita')),
        dbc.ModalBody([
            dbc.Row([
                    dbc.Col([
                        dbc.Label('Description: '),
                        dbc.Input(
                            placeholder="Ex.: Stock Exchange Dividends, Inheritance...", id="txt-revenue"),
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Value: "),
                        dbc.Input(placeholder="Ex.: $100.00",
                                  id='value_revenue', value="")
                    ], width=6)
                    ]),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id='date-revenues',
                                         min_date_allowed=date(
                                             2020, 1, 1),
                                         max_date_allowed=date(
                                             2030, 12, 31),
                                         date=datetime.today(),
                                         style={"width": "100%"}
                                         ),
                ], width=4),

                dbc.Col([
                    dbc.Label("Extras"),
                    dbc.Checklist(
                        options=[{"label": "Foi recebida", "value": 1},
                                 {"label": "Receita Recorrente", "value": 2}],
                        value=[1],
                        id="switches-input-revenue",
                        switch=True),
                ], width=4),

                dbc.Col([
                    html.Label("Categoria da revenue"),
                    dbc.Select(id="select_revenue",
                               options=[{"label": i, "value": i}
                                        for i in cat_revenue],
                               value=cat_revenue[0])
                ], width=4)
            ], style={"margin-top": "25px"}),

            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                    html.Legend("Add category", style={
                                                'color': 'green'}),
                                    dbc.Input(
                                        type="text", placeholder="Nova category...", id="input-add-revenue", value=""),
                                    html.Br(),
                                    dbc.Button(
                                        "Add", className="btn btn-success", id="add-category-revenue", style={"margin-top": "20px"}),
                                    html.Br(),
                                    html.Div(
                                        id="category-div-add-revenue", style={}),
                                    ], width=6, style={'padding-right': '20px'}),

                            dbc.Col([
                                    html.Legend("Excluir categories", style={
                                                'color': 'red'}),
                                    dbc.Checklist(
                                        id="checklist-selected-style-revenue",
                                        options=[{"label": i, "value": i}
                                                 for i in cat_revenue],
                                        value=[],
                                        label_checked_style={
                                            "color": "red"},
                                        input_checked_style={"backgroundColor": "#fa7268",
                                                             "borderColor": "#ea6258"},
                                    ),
                                    dbc.Button(
                                        "Delete", color="warning", id="remove-category-revenue", style={"margin-top": "20px"}),
                                    ], width=6),

                        ])
                    ], title="Add/Delete Categories")

                ], flush=True, start_collapsed=True, id='accordion-revenue'),

                html.Div(id="id_teste_revenue", style={
                    "padding-top": "20px"}),

                dbc.ModalFooter([
                    dbc.Button(
                        "Add Receita", id="salvar_revenue", color="success"),
                    dbc.Popover(dbc.PopoverBody(
                        "Receita Salva"), target="salvar_revenue", placement="left", trigger="click"),
                ])

            ], style={"margin-top": "25px"})

        ])

    ],
        style={"background-color": "rgba(17, 140, 79, 0.05)"},
        id='modal-new-revenue',
        size="lg",
        is_open=False,
        centered=True,
        backdrop=True),

    ### Modal expense ###
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Add expense')),
        dbc.ModalBody([

            dbc.Row([
                dbc.Col([
                    dbc.Label("Description: "),
                    dbc.Input(
                        placeholder="Ex.: Conta de luz, Compra de sapatos...", id="txt-expense"),
                ], width=6),
                dbc.Col([
                    dbc.Label("Value: "),
                    dbc.Input(placeholder="Ex.: $100.00",
                              id="value_expense", value="")
                ], width=6)
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id='date-expenses',
                                         min_date_allowed=date(2020, 1, 1),
                                         max_date_allowed=date(2030, 12, 31),
                                         date=datetime.today(),
                                         style={"width": "100%"}
                                         ),
                ], width=4),

                dbc.Col([
                    dbc.Label("Opções Extras"),
                    dbc.Checklist(
                        options=[{'label': 'Foi recebida', 'value': 1},
                                 {'label': 'Receita Recorrente', 'value': 2}],
                        value=[1],
                        id="switches-input-expense",
                        switch=True),
                ], width=4),

                dbc.Col([
                    html.Label("Categoria da expense"),
                    dbc.Select(id="select_expense",
                               options=[{"label": i, "value": i}
                                        for i in cat_expense],
                               value=cat_expense[0])
                ], width=4),
            ], style={"margin-top": "25px"}),

            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Add category", style={
                                    'color': 'green'}),
                                dbc.Input(
                                    type="text", placeholder="Nova category...", id="input-add-expense", value=""),
                                html.Br(),
                                dbc.Button("Add", className="btn btn-success",
                                           id="add-category-expense", style={"margin-top": "20px"}),
                                html.Br(),
                                html.Div(
                                    id="category-div-add-expense", style={}),
                            ], width=6, style={'padding-right': '20px'}),

                            dbc.Col([
                                html.Legend("Delete categories", style={
                                    'color': 'red'}),
                                dbc.Checklist(
                                    id="checklist-selected-style-expense",
                                    options=[{"label": i, "value": i}
                                             for i in cat_expense],
                                    value=[],
                                    label_checked_style={
                                        "color": "red"},
                                    input_checked_style={"backgroundColor": "#fa7268",
                                                         "borderColor": "#ea6258"},
                                ),
                                dbc.Button(
                                    "Delete", color="warning", id="remove-category-expense", style={"margin-top": "20px"}),
                            ], width=6)
                        ]),
                    ], title="Add/Delete Categories",
                    ),
                ], flush=True, start_collapsed=True, id='accordion-expense'),

                dbc.ModalFooter([
                    dbc.Button("Add expense", color="danger",
                               id="salvar_expense", value="expense"),
                    dbc.Popover(dbc.PopoverBody(
                        "Despesa Salva"), target="salvar_expense", placement="left", trigger="click"),
                ]
                )
            ], style={"margin-top": "25px"}),

        ])
    ], id='modal-new-expense',
        size="lg",
        is_open=False,
        centered=True,
        backdrop=True,
        style={"background-color": "rgba(17, 140, 79, 0.05)"}),

    # seção de navegação--------------------
    html.Hr(),
    dcc.Location(id='url', refresh=False),
    dbc.Nav([
        dbc.NavItem(dbc.NavLink(
            "Dashboard", href="/dashboards", active="exact", id="dashboard-link")),
        dbc.NavItem([
            dbc.NavLink("Statements", id="statements-toggle", active="exact")], id="statements-link"),
        dbc.Collapse([
            dbc.NavLink("Expenses Analysis",
                        href="/analysis-expenses", active="exact", style={"marginLeft": "20px", "fontSize": "0.9em"}, id="expenses-link"),
            dbc.NavLink("Revenue Analysis",
                        href="/analysis-revenues", active="exact", style={"marginLeft": "20px", "fontSize": "0.9em"}, id="revenues-link"),
        ], id="statements-collapse", is_open=False),
    ], vertical=True, id='nav-buttons', style={'margin-bottom': '50px'})

], id='sidebar_inteira')


# =========  Callbacks  =========== #

# # Toggle statements menu collapse com o mouse hover
@app.callback(
    Output("statements-collapse", "is_open"),
    [Input("statements-toggle", "n_clicks"),
     Input('url', 'pathname')],  # Nova entrada
    [State("statements-collapse", "is_open")],
)
def toggle_collapse(n, pathname, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger_id = 'No clicks yet'
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == "statements-toggle":
        return not is_open
    elif trigger_id == 'url':
        if pathname == "/analysis-expenses" or pathname == "/analysis-revenues":
            return True
        elif pathname == "/dashboards":
            return False
    return is_open


# pintar o menu de acordo com a página atual


@app.callback(
    [Output("statements-toggle", "className"),
     Output("dashboard-link", "className"),
     Output("expenses-link", "className"),
     Output("revenues-link", "className")],
    [Input('url', 'pathname')]
)
def update_class(pathname):
    statements_class = ""
    dashboard_class = ""
    expenses_class = ""
    revenues_class = ""

    if pathname == "/dashboards" or pathname == "/":
        dashboard_class = "active-singlelink"
    elif pathname == "/analysis-expenses":
        statements_class = "active-grouplink"
        expenses_class = "active-sublink"
    elif pathname == "/analysis-revenues":
        statements_class = "active-grouplink"
        revenues_class = "active-sublink"

    return statements_class, dashboard_class, expenses_class, revenues_class

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


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def upload_file(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = b64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        print(df.head())

# Pop-up revenue


@ app.callback(
    Output('modal-new-revenue', 'is_open'),
    Input('new-revenue', 'n_clicks'),
    State('modal-new-revenue', 'is_open')
)
def toggle_modal_revenue(n1, is_open):
    if n1:
        return not is_open

# Pop-up expense


@ app.callback(
    Output('modal-new-expense', 'is_open'),
    Input('new-expense', 'n_clicks'),
    State('modal-new-expense', 'is_open')
)
def toggle_modal_expense(n1, is_open):
    if n1:
        return not is_open


# # Pop-up perfis
# @app.callback(
#     Output("modal-perfil", "is_open"),
#     Input("botao_avatar", "n_clicks"),
#     State("modal-perfil", "is_open")
# )
# def toggle_modal(n1, is_open):
#     if n1:
#         return not is_open

# # Enviar nova revenue
@app.callback(
    Output('store-revenues', 'data'),

    Input('salvar_revenue', 'n_clicks'),

    [
        State("txt-revenue", "value"),
        State("value_revenue", "value"),
        State("date-revenues", "date"),
        State("switches-input-revenue", "value"),
        State("select_revenue", "value"),
        State('store-revenues', 'data')
    ]
)
def salve_form_revenue(n, descricao, value, date, switches, category, dict_revenues):

    if n and not (value == "" or value == None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category

        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        df_revenues.loc[df_revenues.shape[0]] = [
            value, recebido, fixo, date, category, descricao]
        df_revenues.to_csv(os.path.join(
            path_data_files, data_files['revenues']))

    data_return = df_revenues.to_dict()
    return data_return

# # Enviar nova expense


@app.callback(
    Output('store-expenses', 'data'),

    Input('salvar_expense', 'n_clicks'),

    [
        State("txt-expense", "value"),
        State("value_expense", "value"),
        State("date-expenses", "date"),
        State("switches-input-expense", "value"),
        State("select_expense", "value"),
        State('store-expenses', 'data')
    ]
)
def salve_form_expense(n, descricao, value, date, switches, category, dict_expenses):
    # import pdb
    # pdb.set_trace()

    if n and not (value == "" or value == None):
        value = round(float(value), 2)
        date = pd.to_datetime(date).date()
        category = category[0] if type(category) == list else category

        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        df_expenses.loc[df_expenses.shape[0]] = [
            value, recebido, fixo, date, category, descricao]
        df_expenses.to_csv(os.path.join(
            path_data_files, data_files['expenses']))

    data_return = df_expenses.to_dict()
    return data_return


# Add/Remove category revenue
@app.callback(
    [Output("select_revenue", "options"),
     Output('checklist-selected-style-revenue', 'options'),
     Output('checklist-selected-style-revenue', 'value'),
     Output('stored-cat-revenues', 'data')
     ],

    # # caso queira adicionar o style e o texto de confirmação no modal faça:
    # [Output("category-div-add-revenue", "children"),
    #  Output("category-div-add-revenue", "style"),
    #  Output("select_revenue", "options"),
    #  Output('checklist-selected-style-revenue', 'options'),
    #  Output('checklist-selected-style-revenue', 'value'),
    #  Output('stored-cat-revenues', 'data')],
    # # não esqueça de adicionar na função essa mudança e também no return


    [Input("add-category-revenue", "n_clicks"),
     Input("remove-category-revenue", 'n_clicks')],

    [State("input-add-revenue", "value"),
     State('checklist-selected-style-revenue', 'value'),
     State('stored-cat-revenues', 'data')]
)
def add_category_revenue(n, n2, txt, check_delete, data):
    cat_revenue = list(data["Categoria"].values())

    # txt1 = []
    # style1 = {}

    # #  Adiciona uma mensagem caso o campo texto esteja vazio
    # if n:
    #     if txt == "" or txt == None:
    #         txt1 = "O campo de texto não pode estar vazio para o registro de uma nova category."
    #         style1 = {'color': 'red'}

    if n and not (txt == "" or txt == None):
        cat_revenue = cat_revenue + \
            [txt] if txt not in cat_revenue else cat_revenue
        # # Adiciona o estilo e a mensagem de confirmação
        # txt1 = f'A category {txt} foi adicionada com sucesso!'
        # style1 = {'color': 'green'}

    if n2:
        if len(check_delete) > 0:
            cat_revenue = [i for i in cat_revenue if i not in check_delete]

    opt_revenue = [{"label": i, "value": i} for i in cat_revenue]
    df_cat_revenue = pd.DataFrame(cat_revenue, columns=['Categoria'])
    df_cat_revenue.to_csv(os.path.join(
        path_data_files, data_files['categories_revenues']))
    data_return = df_cat_revenue.to_dict()

    return [opt_revenue, opt_revenue, [], data_return]
    # se quiser adicionar o style1 e txt1 dentro do modal faça:
    # return [txt1, style1, opt_revenue, opt_revenue, [], data_return]


# Add/Remove category expense
@app.callback(
    [
        Output("select_expense", "options"),
        Output('checklist-selected-style-expense', 'options'),
        Output('checklist-selected-style-expense', 'value'),
        Output('stored-cat-expenses', 'data')],

    # caso queira adicionar o style e o texto de confirmação no modal faça:
    # [Output("category-div-add-expense", "children"),
    #  Output("category-div-add-expense", "style"),
    #  Output("select_expense", "options"),
    #  Output('checklist-selected-style-expense', 'options'),
    #  Output('checklist-selected-style-expense', 'value'),
    #  Output('stored-cat-expenses', 'data')],

    [Input("add-category-expense", "n_clicks"),
     Input("remove-category-expense", 'n_clicks')],

    [State("input-add-expense", "value"),
     State('checklist-selected-style-expense', 'value'),
     State('stored-cat-expenses', 'data')]
)
def add_category_expense(n, n2, txt, check_delete, data):
    cat_expense = list(data["Categoria"].values())

    # # Cria as variáveis para texto de confirmação e estilo do texto
    # txt1 = []
    # style1 = {}

    # #  Adiciona uma mensagem caso o campo texto esteja vazio
    # if n:
    #     if txt == "" or txt == None:
    #         txt1 = "O campo de texto não pode estar vazio para o registro de uma nova category."
    #         style1 = {'color': 'red'}

    if n and not (txt == "" or txt == None):
        cat_expense = cat_expense + \
            [txt] if txt not in cat_expense else cat_expense
        # # Adiciona o estilo e a mensagem de confirmação
        # txt1 = f'A category {txt} foi adicionada com sucesso!'
        # style1 = {'color': 'green'}

    if n2:
        if len(check_delete) > 0:
            cat_expense = [i for i in cat_expense if i not in check_delete]

    opt_expense = [{"label": i, "value": i} for i in cat_expense]
    df_cat_expense = pd.DataFrame(cat_expense, columns=['Categoria'])
    df_cat_expense.to_csv(os.path.join(
        path_data_files, data_files['categories_expenses']))
    data_return = df_cat_expense.to_dict()

    return [opt_expense, opt_expense, [], data_return]
    # # se quiser adicionar o style1 e txt1 dentro do modal faça:
    # return [txt1, style1, opt_expense, opt_expense, [], data_return]
