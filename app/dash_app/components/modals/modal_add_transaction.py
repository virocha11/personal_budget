from datetime import datetime, date
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output   
   
    ### Modal receita ###
    # dbc.Modal([
    #     dbc.ModalHeader(dbc.ModalTitle('Adicionar Receita')),
    #     dbc.ModalBody([
    #         dbc.Row([
    #                 dbc.Col([
    #                     dbc.Label('Descrição: '),
    #                     dbc.Input(
    #                         placeholder="Ex.: dividendos da bolsa, herança...", id="txt-receita"),
    #                 ], width=6),
    #                 dbc.Col([
    #                     dbc.Label("Valor: "),
    #                     dbc.Input(placeholder="Ex.: $100.00",
    #                               id='valor_receita', value="")
    #                 ], width=6)
    #                 ]),

    #         dbc.Row([
    #             dbc.Col([
    #                 dbc.Label("Data: "),
    #                 dcc.DatePickerSingle(id='date-receitas',
    #                                      min_date_allowed=date(
    #                                          2020, 1, 1),
    #                                      max_date_allowed=date(
    #                                          2030, 12, 31),
    #                                      date=datetime.today(),
    #                                      style={"width": "100%"}
    #                                      ),
    #             ], width=4),

    #             dbc.Col([
    #                 dbc.Label("Extras"),
    #                 dbc.Checklist(
    #                     options=[{"label": "Foi recebida", "value": 1},
    #                              {"label": "Receita Recorrente", "value": 2}],
    #                     value=[1],
    #                     id="switches-input-receita",
    #                     switch=True),
    #             ], width=4),

    #             dbc.Col([
    #                 html.Label("Categoria da receita"),
    #                 dbc.Select(id="select_receita",
    #                            options=[{"label": i, "value": i}
    #                                     for i in cat_receita],
    #                            value=cat_receita[0])
    #             ], width=4)
    #         ], style={"margin-top": "25px"}),

    #         dbc.Row([
    #             dbc.Accordion([
    #                 dbc.AccordionItem(children=[
    #                     dbc.Row([
    #                         dbc.Col([
    #                                 html.Legend("Adicionar categoria", style={
    #                                             'color': 'green'}),
    #                                 dbc.Input(
    #                                     type="text", placeholder="Nova categoria...", id="input-add-receita", value=""),
    #                                 html.Br(),
    #                                 dbc.Button(
    #                                     "Adicionar", className="btn btn-success", id="add-category-receita", style={"margin-top": "20px"}),
    #                                 html.Br(),
    #                                 html.Div(
    #                                     id="category-div-add-receita", style={}),
    #                                 ], width=6, style={'padding-right': '20px'}),

    #                         dbc.Col([
    #                                 html.Legend("Excluir categorias", style={
    #                                             'color': 'red'}),
    #                                 dbc.Checklist(
    #                                     id="checklist-selected-style-receita",
    #                                     options=[{"label": i, "value": i}
    #                                              for i in cat_receita],
    #                                     value=[],
    #                                     label_checked_style={
    #                                         "color": "red"},
    #                                     input_checked_style={"backgroundColor": "#fa7268",
    #                                                          "borderColor": "#ea6258"},
    #                                 ),
    #                                 dbc.Button(
    #                                     "Remover", color="warning", id="remove-category-receita", style={"margin-top": "20px"}),
    #                                 ], width=6),

    #                     ])
    #                 ], title="Adicionar/Remover Categorias")

    #             ], flush=True, start_collapsed=True, id='accordion-receita'),

    #             html.Div(id="id_teste_receita", style={
    #                 "padding-top": "20px"}),

    #             dbc.ModalFooter([
    #                 dbc.Button(
    #                     "Adicionar Receita", id="salvar_receita", color="success"),
    #                 dbc.Popover(dbc.PopoverBody(
    #                     "Receita Salva"), target="salvar_receita", placement="left", trigger="click"),
    #             ])

    #         ], style={"margin-top": "25px"})

    #     ])

    # ],
    #     style={"background-color": "rgba(17, 140, 79, 0.05)"},
    #     id='modal-new-receita',
    #     size="lg",
    #     is_open=False,
    #     centered=True,
    #     backdrop=True),
    ### Modal despesa ###
    # dbc.Modal([
    #     dbc.ModalHeader(dbc.ModalTitle('Adicionar despesa')),
    #     dbc.ModalBody([

    #         dbc.Row([
    #             dbc.Col([
    #                 dbc.Label("Descrição: "),
    #                 dbc.Input(
    #                     placeholder="Ex.: Conta de luz, Compra de sapatos...", id="txt-despesa"),
    #             ], width=6),
    #             dbc.Col([
    #                 dbc.Label("Valor: "),
    #                 dbc.Input(placeholder="Ex.: $100.00",
    #                           id="valor_despesa", value="")
    #             ], width=6)
    #         ]),

    #         dbc.Row([
    #             dbc.Col([
    #                 dbc.Label("Data: "),
    #                 dcc.DatePickerSingle(id='date-despesas',
    #                                      min_date_allowed=date(2020, 1, 1),
    #                                      max_date_allowed=date(2030, 12, 31),
    #                                      date=datetime.today(),
    #                                      style={"width": "100%"}
    #                                      ),
    #             ], width=4),

    #             dbc.Col([
    #                 dbc.Label("Opções Extras"),
    #                 dbc.Checklist(
    #                     options=[{'label': 'Foi recebida', 'value': 1},
    #                              {'label': 'Receita Recorrente', 'value': 2}],
    #                     value=[1],
    #                     id="switches-input-despesa",
    #                     switch=True),
    #             ], width=4),

    #             dbc.Col([
    #                 html.Label("Categoria da despesa"),
    #                 dbc.Select(id="select_despesa",
    #                            options=[{"label": i, "value": i}
    #                                     for i in cat_despesa],
    #                            value=cat_despesa[0])
    #             ], width=4),
    #         ], style={"margin-top": "25px"}),

    #         dbc.Row([
    #             dbc.Accordion([
    #                 dbc.AccordionItem(children=[
    #                     dbc.Row([
    #                         dbc.Col([
    #                             html.Legend("Adicionar categoria", style={
    #                                 'color': 'green'}),
    #                             dbc.Input(
    #                                 type="text", placeholder="Nova categoria...", id="input-add-despesa", value=""),
    #                             html.Br(),
    #                             dbc.Button("Adicionar", className="btn btn-success",
    #                                        id="add-category-despesa", style={"margin-top": "20px"}),
    #                             html.Br(),
    #                             html.Div(
    #                                 id="category-div-add-despesa", style={}),
    #                         ], width=6, style={'padding-right': '20px'}),

    #                         dbc.Col([
    #                             html.Legend("Excluir categorias", style={
    #                                 'color': 'red'}),
    #                             dbc.Checklist(
    #                                 id="checklist-selected-style-despesa",
    #                                 options=[{"label": i, "value": i}
    #                                          for i in cat_despesa],
    #                                 value=[],
    #                                 label_checked_style={
    #                                     "color": "red"},
    #                                 input_checked_style={"backgroundColor": "#fa7268",
    #                                                      "borderColor": "#ea6258"},
    #                             ),
    #                             dbc.Button(
    #                                 "Remover", color="warning", id="remove-category-despesa", style={"margin-top": "20px"}),
    #                         ], width=6)
    #                     ]),
    #                 ], title="Adicionar/Remover Categorias",
    #                 ),
    #             ], flush=True, start_collapsed=True, id='accordion-despesa'),

    #             dbc.ModalFooter([
    #                 dbc.Button("Adicionar despesa", color="danger",
    #                            id="salvar_despesa", value="despesa"),
    #                 dbc.Popover(dbc.PopoverBody(
    #                     "Despesa Salva"), target="salvar_despesa", placement="left", trigger="click"),
    #             ]
    #             )
    #         ], style={"margin-top": "25px"}),

    #     ])
    # ], id='modal-new-despesa',
    #     size="lg",
    #     is_open=False,
    #     centered=True,
    #     backdrop=True,
    #     style={"background-color": "rgba(17, 140, 79, 0.05)"}),

## create generic modal to add transactions expenses and revenues
def modal_add_transaction(id, title, categories):
    modal = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(title)),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição: '),
                    dbc.Input(placeholder=f"Ex.: {title.lower()}...", id=f"txt-{id}"),
                ], width=6),
                dbc.Col([
                    dbc.Label("Valor: "),
                    dbc.Input(placeholder="Ex.: $100.00",
                              id=f'valor_{id}', value="")
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Data: "),
                    dcc.DatePickerSingle(id=f'date-{id}',
                                         min_date_allowed=date(2020, 1, 1),
                                         max_date_allowed=date(2030, 12, 31),
                                         date=datetime.today(),
                                         style={"width": "100%"}
                                         ),
                ], width=4),
                dbc.Col([
                    dbc.Label("Extras"),
                    dbc.Checklist(
                        options=[
                            {"label": "Foi recebida", "value": 1},
                            {"label": "Recorrente", "value": 2}
                        ],
                        value=[1],
                        id=f"switches-input-{id}",
                        switch=True),
                ], width=4),
                dbc.Col([
                    dbc.Label("Categoria"),
                    dbc.Select(id=f"select_{id}",
                               options=[{"label": i, "value": i} for i in categories],
                               value=categories[0])
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
                                        type="text", placeholder="Nova categoria...", id=f"input-add-{id}", value=""),
                                    html.Br(),
                                    dbc.Button(
                                        "Adicionar", className="btn btn-success", id=f"add-category-{id}", style={"margin-top": "20px"}),
                                    html.Br(),
                                    html.Div(
                                        id=f"category-div-add-{id}", style={}),
                                    ], width=6, style={'padding-right': '20px'}),
                            dbc.Col([
                                    html.Legend("Excluir categorias", style={
                                                'color': 'red'}),
                                    dbc.Checklist(
                                        id=f"checklist-selected-style-{id}",
                                        options=[{"label": i, "value": i}
                                                for i in categories],
                                        value=[],
                                        label_checked_style={
                                            "color": "red"},
                                        input_checked_style={"backgroundColor": "#fa7268",
                                                                "borderColor": "#ea6258"},
                                    ),
                                    dbc.Button(
                                        "Remover", color="warning", id=f"remove-category-{id}", style={"margin-top": "20px"}),
                                    ], width=6),
                        ])
                    ], title="Adicionar/Remover Categorias")
                ], flush=True, start_collapsed=True, id=f'accordion-{id}'),
                
                html.Div(id=f"id_teste_{id}", style={
                    "padding-top": "20px"}),
                
                dbc.ModalFooter([
                    dbc.Button(
                        f"Adicionar {title}", id=f"salvar_{id}", color="success"),
                    dbc.Popover(dbc.PopoverBody(
                        f"{title} Salva"), target=f"salvar_{id}", placement="left", trigger="click"),
                ])
                
            ], style={"margin-top": "25px"})
        ])
    ],
        style={"background-color": "rgba(17, 140, 79, 0.05)"},
        id=f'modal-new-{id}',
        size="lg",
        is_open=False,
        centered=True,
        backdrop=True)
    return modal