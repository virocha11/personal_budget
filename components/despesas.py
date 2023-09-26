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
        html.Legend("Expenses Table"),
        html.Div(id="tabela-despesas"),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='bar-graph-despesas', style={"margin-right": "20px"}, config={'displayModeBar': False}),
        ], width=9),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Total Expense"),
                    html.Legend("$ -", id="valor_despesa_card",
                                style={'font-size': '3rem'}),
                    html.H6("Total de despesas"),
                ], style={'text-align': 'center', 'padding-top': '30px'}))
        ], width=3),
    ], style={'align-items': 'center'}),

], style={"padding": "10px"})

# =========  Callbacks  =========== #
# Tabela


@app.callback(
    Output('tabela-despesas', 'children'),
    Input('store-despesas', 'data')
)
def imprimir_tabela(data):
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    df.loc[df['Completed'] == 0, 'Completed'] = 'Não'
    df.loc[df['Completed'] == 1, 'Completed'] = 'Sim'

    df.loc[df['Fixed'] == 0, 'Fixed'] = 'Não'
    df.loc[df['Fixed'] == 1, 'Fixed'] = 'Sim'

    df = df.fillna('-')

    df.sort_values(by='Date', ascending=False)
    # coloca a coluna descrição na primeira posição
    cols = df.columns.tolist()
    # cols = cols[-1:] + cols[:-1]
    df = df[cols]

    tabela = dash_table.DataTable(
        id='datatable-despesa-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False,
                "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixed" or i == "Completed"
            else {
                "name": i, "id": i, "deletable": False, "selectable": False,
                "type": "numeric", "format": FormatTemplate.money(2)
            } if i == "Value"
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
                'if': {'column_id': 'Completed',
                       'filter_query': '{Completed} eq "Não"'},
                'backgroundColor': 'tomato',
                'color': 'white'
            },
            {
                'if': {'column_id': 'Completed',
                       'filter_query': '{Completed} eq "Sim"'},
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
    Output('bar-graph-despesas', 'figure'),
    [Input('store-despesas', 'data')]
)
def bar_chart(data):
    df = pd.DataFrame(data)
    df_grouped = df.groupby("Category").sum()[["Value"]].reset_index()
    graph = px.bar(df_grouped, x='Category', y='Value', title="General Expenses",
                   color='Category',  # Adiciona cores
                   # Rótulos dos eixos
                   labels={'Value': 'Value ($)', 'Category': 'Category'},
                   )

    # Atualiza o layout
    graph.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Category",
        yaxis_title="Value ($)",
        yaxis=dict(
            tickprefix="$ ",  # PreFixed para o eixo Y
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
    Output('valor_despesa_card', 'children'),
    Input('store-despesas', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    valor = df['Value'].sum()

    return f"$ {valor}"
