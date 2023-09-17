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
        html.H1("Budget", className="display-5 text-primary fw-bolder mt-3"),
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

    dbc.Modal(
        [
            dbc.ModalHeader("Importar CSV"),
            dbc.ModalBody(
                dcc.Upload(
                    id='upload-data',
                    children=html.Button('Selecione o arquivo CSV'),
                    multiple=False
                )
            ),
            dbc.ModalFooter(
                dbc.Button("Fechar", id="close-button", className="ml-auto")
            ),
        ],
        id="import-modal",
    ),
    ### Modal receita ###
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar Receita')),
        dbc.ModalBody([
            dbc.Row([
                    dbc.Col([
                        dbc.Label('Descrição: '),
                        dbc.Input(
                            placeholder="Ex.: dividendos da bolsa, herança...", id="txt-receita"),
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Valor: "),
                        dbc.Input(placeholder="Ex.: $100.00",
                                  id='valor_receita', value="")
                    ], width=6)
                    ]),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id='date-receitas',
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
                        id="switches-input-receita",
                        switch=True),
                ], width=4),

                dbc.Col([
                    html.Label("Categoria da receita"),
                    dbc.Select(id="select_receita",
                               options=[{"label": i, "value": i}
                                        for i in cat_receita],
                               value=cat_receita[0])
                ], width=4)
            ], style={"margin-top": "25px"}),

            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                    html.Legend("Adicionar categoria", style={
                                                'color': 'green'}),
                                    dbc.Input(
                                        type="text", placeholder="Nova categoria...", id="input-add-receita", value=""),
                                    html.Br(),
                                    dbc.Button(
                                        "Adicionar", className="btn btn-success", id="add-category-receita", style={"margin-top": "20px"}),
                                    html.Br(),
                                    html.Div(
                                        id="category-div-add-receita", style={}),
                                    ], width=6, style={'padding-right': '20px'}),

                            dbc.Col([
                                    html.Legend("Excluir categorias", style={
                                                'color': 'red'}),
                                    dbc.Checklist(
                                        id="checklist-selected-style-receita",
                                        options=[{"label": i, "value": i}
                                                 for i in cat_receita],
                                        value=[],
                                        label_checked_style={
                                            "color": "red"},
                                        input_checked_style={"backgroundColor": "#fa7268",
                                                             "borderColor": "#ea6258"},
                                    ),
                                    dbc.Button(
                                        "Remover", color="warning", id="remove-category-receita", style={"margin-top": "20px"}),
                                    ], width=6),

                        ])
                    ], title="Adicionar/Remover Categorias")

                ], flush=True, start_collapsed=True, id='accordion-receita'),

                html.Div(id="id_teste_receita", style={
                    "padding-top": "20px"}),

                dbc.ModalFooter([
                    dbc.Button(
                        "Adicionar Receita", id="salvar_receita", color="success"),
                    dbc.Popover(dbc.PopoverBody(
                        "Receita Salva"), target="salvar_receita", placement="left", trigger="click"),
                ])

            ], style={"margin-top": "25px"})

        ])

    ],
        style={"background-color": "rgba(17, 140, 79, 0.05)"},
        id='modal-new-receita',
        size="lg",
        is_open=False,
        centered=True,
        backdrop=True),

    ### Modal despesa ###
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
        dbc.ModalBody([

            dbc.Row([
                dbc.Col([
                    dbc.Label("Descrição: "),
                    dbc.Input(
                        placeholder="Ex.: Conta de luz, Compra de sapatos...", id="txt-despesa"),
                ], width=6),
                dbc.Col([
                    dbc.Label("Valor: "),
                    dbc.Input(placeholder="Ex.: $100.00",
                              id="valor_despesa", value="")
                ], width=6)
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id='date-despesas',
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
                        id="switches-input-despesa",
                        switch=True),
                ], width=4),

                dbc.Col([
                    html.Label("Categoria da despesa"),
                    dbc.Select(id="select_despesa",
                               options=[{"label": i, "value": i}
                                        for i in cat_despesa],
                               value=cat_despesa[0])
                ], width=4),
            ], style={"margin-top": "25px"}),

            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar categoria", style={
                                    'color': 'green'}),
                                dbc.Input(
                                    type="text", placeholder="Nova categoria...", id="input-add-despesa", value=""),
                                html.Br(),
                                dbc.Button("Adicionar", className="btn btn-success",
                                           id="add-category-despesa", style={"margin-top": "20px"}),
                                html.Br(),
                                html.Div(
                                    id="category-div-add-despesa", style={}),
                            ], width=6, style={'padding-right': '20px'}),

                            dbc.Col([
                                html.Legend("Excluir categorias", style={
                                    'color': 'red'}),
                                dbc.Checklist(
                                    id="checklist-selected-style-despesa",
                                    options=[{"label": i, "value": i}
                                             for i in cat_despesa],
                                    value=[],
                                    label_checked_style={
                                        "color": "red"},
                                    input_checked_style={"backgroundColor": "#fa7268",
                                                         "borderColor": "#ea6258"},
                                ),
                                dbc.Button(
                                    "Remover", color="warning", id="remove-category-despesa", style={"margin-top": "20px"}),
                            ], width=6)
                        ]),
                    ], title="Adicionar/Remover Categorias",
                    ),
                ], flush=True, start_collapsed=True, id='accordion-despesa'),

                dbc.ModalFooter([
                    dbc.Button("Adicionar despesa", color="danger",
                               id="salvar_despesa", value="despesa"),
                    dbc.Popover(dbc.PopoverBody(
                        "Despesa Salva"), target="salvar_despesa", placement="left", trigger="click"),
                ]
                )
            ], style={"margin-top": "25px"}),

        ])
    ], id='modal-new-despesa',
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

# Pop-up receita


@ app.callback(
    Output('modal-new-receita', 'is_open'),
    Input('new-receita', 'n_clicks'),
    State('modal-new-receita', 'is_open')
)
def toggle_modal_receita(n1, is_open):
    if n1:
        return not is_open

# Pop-up despesa


@ app.callback(
    Output('modal-new-despesa', 'is_open'),
    Input('new-despesa', 'n_clicks'),
    State('modal-new-despesa', 'is_open')
)
def toggle_modal_despesa(n1, is_open):
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

# # Enviar nova receita
@app.callback(
    Output('store-receitas', 'data'),

    Input('salvar_receita', 'n_clicks'),

    [
        State("txt-receita", "value"),
        State("valor_receita", "value"),
        State("date-receitas", "date"),
        State("switches-input-receita", "value"),
        State("select_receita", "value"),
        State('store-receitas', 'data')
    ]
)
def salve_form_receita(n, descricao, valor, date, switches, categoria, dict_receitas):

    if n and not (valor == "" or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0] if type(categoria) == list else categoria

        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        df_receitas.loc[df_receitas.shape[0]] = [
            valor, recebido, fixo, date, categoria, descricao]
        df_receitas.to_csv(os.path.join(
            path_data_files, data_files['receitas']))

    data_return = df_receitas.to_dict()
    return data_return

# # Enviar nova despesa


@app.callback(
    Output('store-despesas', 'data'),

    Input('salvar_despesa', 'n_clicks'),

    [
        State("txt-despesa", "value"),
        State("valor_despesa", "value"),
        State("date-despesas", "date"),
        State("switches-input-despesa", "value"),
        State("select_despesa", "value"),
        State('store-despesas', 'data')
    ]
)
def salve_form_despesa(n, descricao, valor, date, switches, categoria, dict_despesas):
    # import pdb
    # pdb.set_trace()

    if n and not (valor == "" or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0] if type(categoria) == list else categoria

        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        df_despesas.loc[df_despesas.shape[0]] = [
            valor, recebido, fixo, date, categoria, descricao]
        df_despesas.to_csv(os.path.join(
            path_data_files, data_files['despesas']))

    data_return = df_despesas.to_dict()
    return data_return


# Add/Remove categoria receita
@app.callback(
    [Output("select_receita", "options"),
     Output('checklist-selected-style-receita', 'options'),
     Output('checklist-selected-style-receita', 'value'),
     Output('stored-cat-receitas', 'data')
     ],

    # # caso queira adicionar o style e o texto de confirmação no modal faça:
    # [Output("category-div-add-receita", "children"),
    #  Output("category-div-add-receita", "style"),
    #  Output("select_receita", "options"),
    #  Output('checklist-selected-style-receita', 'options'),
    #  Output('checklist-selected-style-receita', 'value'),
    #  Output('stored-cat-receitas', 'data')],
    # # não esqueça de adicionar na função essa mudança e também no return


    [Input("add-category-receita", "n_clicks"),
     Input("remove-category-receita", 'n_clicks')],

    [State("input-add-receita", "value"),
     State('checklist-selected-style-receita', 'value'),
     State('stored-cat-receitas', 'data')]
)
def add_category_receita(n, n2, txt, check_delete, data):
    cat_receita = list(data["Categoria"].values())

    # txt1 = []
    # style1 = {}

    # #  Adiciona uma mensagem caso o campo texto esteja vazio
    # if n:
    #     if txt == "" or txt == None:
    #         txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
    #         style1 = {'color': 'red'}

    if n and not (txt == "" or txt == None):
        cat_receita = cat_receita + \
            [txt] if txt not in cat_receita else cat_receita
        # # Adiciona o estilo e a mensagem de confirmação
        # txt1 = f'A categoria {txt} foi adicionada com sucesso!'
        # style1 = {'color': 'green'}

    if n2:
        if len(check_delete) > 0:
            cat_receita = [i for i in cat_receita if i not in check_delete]

    opt_receita = [{"label": i, "value": i} for i in cat_receita]
    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_receita.to_csv(os.path.join(
        path_data_files, data_files['categorias_receitas']))
    data_return = df_cat_receita.to_dict()

    return [opt_receita, opt_receita, [], data_return]
    # se quiser adicionar o style1 e txt1 dentro do modal faça:
    # return [txt1, style1, opt_receita, opt_receita, [], data_return]


# Add/Remove categoria despesa
@app.callback(
    [
        Output("select_despesa", "options"),
        Output('checklist-selected-style-despesa', 'options'),
        Output('checklist-selected-style-despesa', 'value'),
        Output('stored-cat-despesas', 'data')],

    # caso queira adicionar o style e o texto de confirmação no modal faça:
    # [Output("category-div-add-despesa", "children"),
    #  Output("category-div-add-despesa", "style"),
    #  Output("select_despesa", "options"),
    #  Output('checklist-selected-style-despesa', 'options'),
    #  Output('checklist-selected-style-despesa', 'value'),
    #  Output('stored-cat-despesas', 'data')],

    [Input("add-category-despesa", "n_clicks"),
     Input("remove-category-despesa", 'n_clicks')],

    [State("input-add-despesa", "value"),
     State('checklist-selected-style-despesa', 'value'),
     State('stored-cat-despesas', 'data')]
)
def add_category_despesa(n, n2, txt, check_delete, data):
    cat_despesa = list(data["Categoria"].values())

    # # Cria as variáveis para texto de confirmação e estilo do texto
    # txt1 = []
    # style1 = {}

    # #  Adiciona uma mensagem caso o campo texto esteja vazio
    # if n:
    #     if txt == "" or txt == None:
    #         txt1 = "O campo de texto não pode estar vazio para o registro de uma nova categoria."
    #         style1 = {'color': 'red'}

    if n and not (txt == "" or txt == None):
        cat_despesa = cat_despesa + \
            [txt] if txt not in cat_despesa else cat_despesa
        # # Adiciona o estilo e a mensagem de confirmação
        # txt1 = f'A categoria {txt} foi adicionada com sucesso!'
        # style1 = {'color': 'green'}

    if n2:
        if len(check_delete) > 0:
            cat_despesa = [i for i in cat_despesa if i not in check_delete]

    opt_despesa = [{"label": i, "value": i} for i in cat_despesa]
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_despesa.to_csv(os.path.join(
        path_data_files, data_files['categorias_despesas']))
    data_return = df_cat_despesa.to_dict()

    return [opt_despesa, opt_despesa, [], data_return]
    # # se quiser adicionar o style1 e txt1 dentro do modal faça:
    # return [txt1, style1, opt_despesa, opt_despesa, [], data_return]
