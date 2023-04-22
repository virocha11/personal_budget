from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


card_icon = {
    'color': 'white',
    'text-align': 'center',
    'font-size': 30,
    'margin': 'auto',
}

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        # Saldo Total
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Saldo'),
                    html.H5('R$ 9.300,00', id='value-saldo-dashboards', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px', 'margin-right': 0}),

                dbc.Card(
                    html.Div(className='fa fa-balance-scale', style=card_icon),
                    color='warning',
                    style={'max-width': 75, 'height': 100},
                )
            ])
        ], width=4),
        # Receita
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Receitas'),
                    html.H5('R$ 15.000,00',
                            id='value-receita-dashboards', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px', 'margin-right': 0}),

                dbc.Card(
                    html.Div(className='fa fa-smile-o', style=card_icon),
                    color='success',
                    style={'max-width': 75, 'height': 100},
                )
            ])
        ], width=4),
        # Despesa
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Despesas'),
                    html.H5('R$ 5.700,00',
                            id='value-despesas-dashboards', style={})
                ], style={'padding-left': '20px', 'padding-top': '10px', 'margin-right': 0}),

                dbc.Card(
                    html.Div(className='fa fa-meh-o', style=card_icon),
                    color='danger',
                    style={'max-width': 75, 'height': 100},
                )
            ])
        ], width=4)
    ], style={"margin": "10px"}),

    dbc.Row([
        dbc.Col([
            dbc.Card([

                html.Legend("Filtrar lançamentos", className="card-title"),

                html.Label("Categorias das receitas"),
                html.Div(
                    dcc.Dropdown(
                        id="dropdown-receita",
                        clearable=False,
                        style={"width": "100%"},
                        persistence=True,
                        persistence_type="session",
                        multi=True)
                ),

                html.Label("Categorias das despesas",
                           style={"margin-top": "10px"}),
                dcc.Dropdown(
                    id="dropdown-despesa",
                    clearable=False,
                    style={"width": "100%"},
                    persistence=True,
                    persistence_type="session",
                    multi=True
                ),
                html.Legend("Período de Análise", style={
                    "margin-top": "10px"}),
                dcc.DatePickerRange(
                    month_format='Do MMM, YY',
                    end_date_placeholder_text='Data...',
                    start_date=datetime.today(),
                    end_date=datetime.today() + timedelta(days=31),
                    with_portal=True,
                    updatemode='singledate',
                    id='date-picker-config',
                    style={'z-index': '100'})

            ], style={"height": "100%", "padding": "20px"})
        ], width=4),

        dbc.Col(dbc.Card(dcc.Graph(id="graph1"), style={
            "height": "100%", "padding": "10px"}), width=8),

    ], style={"margin": "10px"}),

    dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"),
                    style={"padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph3"),
                    style={"padding": "10px"}), width=3),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4"),
                    style={"padding": "10px"}), width=3),
            ], style={"margin": "10px"})

])


# =========  Callbacks  =========== #
# # Dropdown Receita e também card de receita total
@app.callback([Output("dropdown-receita", "options"),
               Output("dropdown-receita", "value"),
               Output("value-receita-dashboards", "children")],
              Input("store-receitas", "data"))
def manage_dropdown_receitas(data):
    df_dropdown_receitas = pd.DataFrame(data)
    valor_receita_total = df_dropdown_receitas['Valor'].sum()
    dropdown_marks = df_dropdown_receitas['Categoria'].unique().tolist()

    return [([{"label": x, "value": x} for x in df_dropdown_receitas['Categoria'].unique()]), dropdown_marks, locale.format_string("R$ %.2f", valor_receita_total, grouping=True)]

# # Dropdown Despesa e também card de despesa total


@app.callback([Output("dropdown-despesa", "options"),
               Output("dropdown-despesa", "value"),
               Output("value-despesas-dashboards", "children")],
              Input("store-despesas", "data"))
def manage_dropdown_despesas(data):
    df_dropdown_despesas = pd.DataFrame(data)
    valor_despesa_total = df_dropdown_despesas['Valor'].sum()
    dropdown_marks = df_dropdown_despesas['Categoria'].unique().tolist()

    return [([{"label": x, "value": x} for x in df_dropdown_despesas['Categoria'].unique()]), dropdown_marks, locale.format_string("R$ %.2f", valor_despesa_total, grouping=True)]

# Card de valor total subtraindo as despesas das receitas


@app.callback(
    Output("value-saldo-dashboards", "children"),
    [Input("store-despesas", "data"),
     Input("store-receitas", "data")])
def saldo_total(despesas, receitas):
    valor_despesas = pd.DataFrame(despesas)['Valor'].sum()
    valor_receitas = pd.DataFrame(receitas)['Valor'].sum()

    valor_saldo = valor_receitas - valor_despesas

    return locale.format_string("R$ %.2f", valor_saldo, grouping=True)
