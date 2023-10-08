import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from dash.dash_table import FormatTemplate
from dash.dash_table.Format import Group, Format, Scheme, Sign, Symbol
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.Legend("Tabela de receitas"),
        html.Div(id="tabela-receitas"),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='bar-graph-receitas', style={"margin-right": "20px"}, config={'displayModeBar': False}),
        ], width=9),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Receitas"),
                    html.Legend("€ -", id="valor_receita_card",
                                style={'font-size': '3rem'}),
                    html.H6("Total de receitas"),
                ], style={'text-align': 'center', 'padding-top': '30px'}))
        ], width=3),
    ], style={'align-items': 'center'}),

], style={"padding": "10px"})

# =========  Callbacks  =========== #
# Tabela


@app.callback(
    Output('tabela-receitas', 'children'),
    Input('store-receitas', 'data')
)
def create_table(data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data']).dt.date

    df.loc[df['Efetuado'] == 0, 'Efetuado'] = 'Não'
    df.loc[df['Efetuado'] == 1, 'Efetuado'] = 'Sim'

    df.loc[df['Fixo'] == 0, 'Fixo'] = 'Não'
    df.loc[df['Fixo'] == 1, 'Fixo'] = 'Sim'

    df = df.fillna('-')

    df.sort_values(by='Data', ascending=False)
    # coloca a coluna descrição na primeira posição
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    tabela = dash_table.DataTable(
        id='datatable-receita-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False,
                "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" or i == "Efetuado"
            else {
                "name": i, "id": i, "deletable": False, "selectable": False,
                "type": "numeric", "format": FormatTemplate.money(2)
            } if i == "Valor"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="single",
        column_selectable=None,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        style_table={'overflowX': 'auto'},  # Scroll horizontal
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
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
            }
        ],
        style_cell={
            'textAlign': 'left',
            'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        filter_options={"placeholder_text": "Filtrar..."},
    ),

    return tabela

# Bar Graph


@app.callback(
    Output('bar-graph-receitas', 'figure'),
    [Input('store-receitas', 'data')]
)
def bar_chart(data):
    df = pd.DataFrame(data)
    df_grouped = df.groupby("Categoria").sum()[["Valor"]].reset_index()
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Receitas Gerais",
                   color='Categoria',  # Adiciona cores
                   # Rótulos dos eixos
                   labels={'Valor': 'Valor (€)', 'Categoria': 'Categoria'},
                   )

    # Atualiza o layout
    graph.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Categoria",
        yaxis_title="Valor (€)",
        yaxis=dict(
            tickprefix="€ ",  # Prefixo para o eixo Y
            title_font=dict(
                size=16,
                color='black',
            ),
        ),
        xaxis=dict(
            title_font=dict(
                size=16,
                color='black',
            ),
        )
    )

    return graph


# Simple card


@app.callback(
    Output('valor_receita_card', 'children'),
    Input('store-receitas', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()

    ## duas casas decimais
    return f"€ {valor:.2f}"
