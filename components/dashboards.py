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
from myindex import app
# import locale
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


card_icon = {
    'color': 'white',
    'text-align': 'center',
    'font-size': 30,
    'margin': 'auto',
}

graph_margin = dict(l=25, r=25, t=25, b=10)

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
                    start_date=datetime.today() - timedelta(days=365),
                    end_date=datetime.today(),
                    with_portal=True,
                    updatemode='singledate',
                    id='date-picker-config',
                    style={'z-index': '100'})

            ], style={"height": "100%", "padding": "20px"})
        ], width=4),

        dbc.Col(dbc.Card(dcc.Graph(id="graph1",
                                   config={
                                       "displayModeBar": True,
                                       "displaylogo": False,
                                       "modeBarButtonsToRemove": ["pan2d", "lasso2d"]
                                   }), style={
            "height": "100%", "padding": "10px"}), width=8),

    ], style={"margin": "10px"}),

    dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph2", config={'displayModeBar': False}),
                    style={"padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph3", config={'displayModeBar': False}),
                    style={"padding": "10px"}), width=3),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4", config={'displayModeBar': False}),
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

    return [([{"label": x, "value": x} for x in df_dropdown_receitas['Categoria'].unique()]), dropdown_marks, f"R$ {valor_receita_total:.2f}"]

# # Dropdown Despesa e também card de despesa total


@app.callback([Output("dropdown-despesa", "options"),
               Output("dropdown-despesa", "value"),
               Output("value-despesas-dashboards", "children")],
              Input("store-despesas", "data"))
def manage_dropdown_despesas(data):
    df_dropdown_despesas = pd.DataFrame(data)
    valor_despesa_total = df_dropdown_despesas['Valor'].sum()
    dropdown_marks = df_dropdown_despesas['Categoria'].unique().tolist()

    return [([{"label": x, "value": x} for x in df_dropdown_despesas['Categoria'].unique()]), dropdown_marks,  f"R$ {valor_despesa_total:.2f}"]

# Card de valor total subtraindo as despesas das receitas


@app.callback(
    Output("value-saldo-dashboards", "children"),
    [Input("store-despesas", "data"),
     Input("store-receitas", "data")])
def saldo_total(despesas, receitas):
    valor_despesas = pd.DataFrame(despesas)['Valor'].sum()
    valor_receitas = pd.DataFrame(receitas)['Valor'].sum()

    valor_saldo = valor_receitas - valor_despesas

    return f"R$ {valor_saldo:.2f}"

# # Gráfico 1


@app.callback(
    Output('graph1', 'figure'),
    [Input('store-despesas', 'data'),
     Input('store-receitas', 'data'),
     Input("dropdown-despesa", "value"),
     Input("dropdown-receita", "value"),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date')])
def atualiza_grafico1(data_despesa, data_receita, despesa, receita, start_date, end_date):
    df_ds = pd.DataFrame(data_despesa).sort_values(by="Data")
    # verifica quais categorias estão marcadas no dropdown-despesas
    # df_ds = df_ds[df_ds['Categoria'].isin(despesa)]
    df_ds = df_ds.groupby("Data").sum(numeric_only=True)
    df_rc = pd.DataFrame(data_receita).sort_values(by="Data")
    # verifica quais categorias estão marcadas no dropdown-receitas
    # df_rc = df_rc[df_rc['Categoria'].isin(receita)]
    df_rc = df_rc.groupby("Data").sum(numeric_only=True)

    df_acum = pd.merge(df_rc[['Valor']], df_ds[['Valor']], on="Data", how="outer", suffixes=(
        '_receitas', '_despesas')).fillna(0).sort_values(by="Data")
    df_acum["Saldo"] = df_acum["Valor_receitas"] - df_acum["Valor_despesas"]
    df_acum["Acumulado"] = df_acum["Saldo"].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name='Fluxo de Caixa', x=df_acum.index, y=df_acum['Acumulado'], mode='lines'))

    fig.update_layout(margin=graph_margin, height=300)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')
    return fig

# # Gráfico 2 Barras das receitas e despesas por data


@app.callback(
    Output('graph2', 'figure'),
    [Input('store-receitas', 'data'),
     Input('store-despesas', 'data'),
     Input('dropdown-receita', 'value'),
     Input('dropdown-despesa', 'value'),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date')]
)
def atualiza_grafico2(data_receita, data_despesa, receita, despesa, start_date, end_date):
    df_ds = pd.DataFrame(data_despesa)
    # verifica quais categorias estão marcadas no dropdown-despesas
    df_ds = df_ds[df_ds['Categoria'].isin(despesa)]
    df_ds = df_ds.groupby("Data", as_index=False).sum(numeric_only=True)
    df_rc = pd.DataFrame(data_receita)
    # verifica quais categorias estão marcadas no dropdown-receitas
    df_rc = df_rc[df_rc['Categoria'].isin(receita)]
    df_rc = df_rc.groupby("Data", as_index=False).sum(numeric_only=True)
    df_rc['Tipo'] = 'Receitas'
    df_ds['Tipo'] = 'Despesas'

    # transforma o dataframa de receitas e despesas em uma tabela única unidos verticalmente
    df_final = pd.concat([df_ds, df_rc], ignore_index=True)

    mask = (df_final['Data'] > start_date) & (df_final['Data'] <= end_date)
    df_final = df_final.loc[mask]

    fig = px.bar(df_final, x="Data", y="Valor",
                 color='Tipo', barmode="group")

    fig.update_layout(margin=graph_margin)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig

# # Gráfico 3


@app.callback(
    Output('graph3', "figure"),
    [Input('store-receitas', 'data'),
     Input('dropdown-receita', 'value'),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date')]
)
def atualiza_grafico_pie_receita(data_receita, receita, start_date, end_date):
    df = pd.DataFrame(data_receita)
    df = df[df['Categoria'].isin(receita)]

    mask = (df['Data'] > start_date) & (df['Data'] <= end_date)
    df = df.loc[mask]

    fig = px.pie(df, values=df['Valor'], names=df["Categoria"], hole=.2)
    fig.update_layout(title={'text': "Receitas"})
    fig.update_layout(margin=graph_margin)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig

# # Gráfico 4


@app.callback(
    Output('graph4', "figure"),
    [Input('store-despesas', 'data'),
     Input('dropdown-despesa', 'value'),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date')]
)
def atualiza_grafico_pie_despesa(data_despesa, despesa,  start_date, end_date):
    df = pd.DataFrame(data_despesa)
    df = df[df['Categoria'].isin(despesa)]

    mask = (df['Data'] > start_date) & (df['Data'] <= end_date)
    df = df.loc[mask]

    fig = px.pie(df, values=df['Valor'], names=df["Categoria"], hole=.2)
    fig.update_layout(title={'text': "Despesas"})

    fig.update_layout(margin=graph_margin)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig
