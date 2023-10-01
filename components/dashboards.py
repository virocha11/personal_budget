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
# locale.setlocale(locale.LC_ALL, 'pt_PT.UTF-8')

card_icon = {
    'color': 'white',
    'textAlign': 'center',
    'font-size': 30,
    'margin': 'auto',
}

graph_margin = dict(l=10, r=10, t=25, b=0, pad=2)

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        # Saldo Total
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Balance',
                                style={'font-size': '1.3rem', 'color': 'black'}),
                    html.H5('$ 9.300,00', id='value-saldo-dashboards',
                            style={'font-size': '1.2rem'})
                ], style={'padding-left': '20px', 'padding-top': '10px', 'margin-right': 0}),

                dbc.Card(
                    html.Div(className='fa fa-balance-scale', style=card_icon),
                    color='warning',
                    style={'max-width': 75, 'height': 90},
                )
            ])
        ], width=4),
        # Receita
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Revenue',
                                style={'font-size': '1.3rem', 'color': 'black'}),
                    html.H5('$ 15.000,00',
                            id='value-revenue-dashboards', style={'font-size': '1.2rem'})
                ], style={'padding-left': '20px', 'padding-top': '10px', 'margin-right': 0}),

                dbc.Card(
                    html.Div(className='fa fa-smile-o', style=card_icon),
                    color='success',
                    style={'max-width': 75, 'height': 90},
                )
            ])
        ], width=4),
        # Expense
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend('Expenses',
                                style={'font-size': '1.3rem', 'color': 'black'}),
                    html.H5('$ 5.700,00',
                            id='value-expenses-dashboards', style={'font-size': '1.2rem'})
                ], style={'padding-left': '20px', 'padding-top': '10px', 'margin-right': 0}),

                dbc.Card(
                    html.Div(className='fa fa-meh-o', style=card_icon),
                    color='danger',
                    style={'max-width': 75, 'height': 90},
                )
            ])
        ], width=4)
    ], style={"margin": "10px"}),

    dbc.Row([
        dbc.Col([
            dbc.Card([

                html.Legend("Filter Categories", className="card-title"),

                html.Label("Categorys das revenues"),
                html.Div(
                    dcc.Dropdown(
                        id="dropdown-revenue",
                        clearable=False,
                        style={"width": "100%"},
                        persistence=True,
                        persistence_type="session",
                        multi=True)
                ),

                html.Label("Categorys das expenses",
                           style={"margin-top": "10px"}),
                dcc.Dropdown(
                    id="dropdown-expense",
                    clearable=False,
                    style={"width": "100%"},
                    persistence=True,
                    persistence_type="session",
                    multi=True
                ),
                html.Legend("Analysis Period", style={
                    "margin-top": "10px"}),
                dcc.DatePickerRange(
                    month_format='DD/MM/YYYY',  # como formato para dia mes ano em portugues = 'DD
                    end_date_placeholder_text='Date...',
                    start_date=datetime.today() - timedelta(days=365),
                    end_date=datetime.today(),
                    updatemode='singledate',
                    id='date-picker-config')
            ], style={"height": "100%", "padding": "20px"})
        ], width=4),

        dbc.Col(dbc.Card(dcc.Graph(id="graph1",
                                   config={
                                       "displayModeBar": False,
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
            dbc.Col(dbc.Card(dcc.Graph(id="graph4", ),
                    style={"padding": "10px"}), width=3),
            ], style={"margin": "10px"})

])


# =========  Callbacks  =========== #
# # Dropdown Receita e também card de revenue total
@app.callback([Output("dropdown-revenue", "options"),
               Output("dropdown-revenue", "value"),
               Output("value-revenue-dashboards", "children")],
              Input("store-revenues", "data"))
def manage_dropdown_revenues(data):
    df_dropdown_revenues = pd.DataFrame(data)
    valor_revenue_total = df_dropdown_revenues['Value'].sum()
    dropdown_marks = df_dropdown_revenues['Category'].unique().tolist()

    return [([{"label": x, "value": x} for x in df_dropdown_revenues['Category'].unique()]), dropdown_marks, locale.format_string("$ %.2f", valor_revenue_total, grouping=True)]

# # Dropdown Expense e também card de expense total


@app.callback([Output("dropdown-expense", "options"),
               Output("dropdown-expense", "value"),
               Output("value-expenses-dashboards", "children")],
              Input("store-expenses", "data"))
def manage_dropdown_expenses(data):
    df_dropdown_expenses = pd.DataFrame(data)
    valor_expense_total = df_dropdown_expenses['Value'].sum()
    dropdown_marks = df_dropdown_expenses['Category'].unique().tolist()

    return [([{"label": x, "value": x} for x in df_dropdown_expenses['Category'].unique()]), dropdown_marks, locale.format_string("$ %.2f", valor_expense_total, grouping=True)]

# Card de valor total subtraindo as expenses das revenues


@app.callback(
    Output("value-saldo-dashboards", "children"),
    [Input("store-expenses", "data"),
     Input("store-revenues", "data")])
def saldo_total(expenses, revenues):
    valor_expenses = pd.DataFrame(expenses)['Value'].sum()
    valor_revenues = pd.DataFrame(revenues)['Value'].sum()

    valor_saldo = valor_revenues - valor_expenses

    return locale.format_string("$ %.2f", valor_saldo, grouping=True)


# Gráfico 1
@app.callback(
    Output('graph1', 'figure'),
    [Input('store-expenses', 'data'),
     Input('store-revenues', 'data'),
     Input("dropdown-expense", "value"),
     Input("dropdown-revenue", "value"),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date')])
def atualiza_grafico1(data_expense, data_revenue, expense, revenue, start_date, end_date):
    
    ## calculate cash flow and acumulated in df_acum
    df_ds = pd.DataFrame(data_expense).sort_values(by="Date")
    # verifica quais categories estão marcadas no dropdown-expenses
    # df_ds = df_ds[df_ds['Category'].isin(expense)]
    df_ds = df_ds.groupby("Date").sum(numeric_only=True)
    df_rc = pd.DataFrame(data_revenue).sort_values(by="Date")
    # verifica quais categories estão marcadas no dropdown-revenues
    # df_rc = df_rc[df_rc['Category'].isin(revenue)]
    df_rc = df_rc.groupby("Date").sum(numeric_only=True)

    df_acum = pd.merge(df_rc[['Value']], df_ds[['Value']], on="Date", how="outer", suffixes=(
        '_revenues', '_expenses')).fillna(0).sort_values(by="Date")
    df_acum["Saldo"] = df_acum["Value_revenues"] - df_acum["Value_expenses"]
    df_acum["Acumulado"] = df_acum["Saldo"].cumsum()

    date_filter = (df_acum.index > start_date) & (df_acum.index <= end_date)
    df_acum = df_acum.loc[date_filter]

    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name='Cash Flow',
        x=df_acum.index,
        y=df_acum['Acumulado'],
        mode='lines',
        line=dict(color='rgb(0, 0, 255)', width=2,
                  smoothing=0.3, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 0, 255, 0.1)',
        hovertemplate='%{y:$,.2f}',
    ))

    fig.update_layout(
        margin=graph_margin,
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            tickformat="$,.2f"
        ),
        xaxis=dict(
            tickmode='auto',
            nticks=len(df_acum.index),
            tickformat='%b %Y'
        )
    )

    return fig

# # Gráfico 2 Barras das revenues e expenses por data


@app.callback(
    Output('graph2', 'figure'),
    [Input('store-revenues', 'data'),
     Input('store-expenses', 'data'),
     Input('dropdown-revenue', 'value'),
     Input('dropdown-expense', 'value'),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date')]
)
def atualiza_grafico2(data_revenue, data_expense, revenue, expense, start_date, end_date):
    df_ds = pd.DataFrame(data_expense)
    # verifica quais categories estão marcadas no dropdown-expenses
    df_ds = df_ds[df_ds['Category'].isin(expense)]
    df_ds = df_ds.groupby("Date", as_index=False).sum(numeric_only=True)
    df_rc = pd.DataFrame(data_revenue)
    # verifica quais categories estão marcadas no dropdown-revenues
    df_rc = df_rc[df_rc['Category'].isin(revenue)]
    df_rc = df_rc.groupby("Date", as_index=False).sum(numeric_only=True)
    df_rc['Type'] = 'Expenses'
    df_ds['Type'] = 'Revenue'

    # transforma o dataframa de revenues e expenses em uma tabela única unidos verticalmente
    df_final = pd.concat([df_ds, df_rc], ignore_index=True)

    date_filter = (df_final['Date'] > start_date) & (
        df_final['Date'] <= end_date)
    df_final = df_final.loc[date_filter]

    fig = px.bar(df_final, x="Date", y="Value",
                 color='Type', barmode="group",
                 )

    fig.update_layout(margin=graph_margin, height=300)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig

# # Gráfico 3


@app.callback(
    Output('graph3', "figure"),
    [Input('store-revenues', 'data'),
     Input('dropdown-revenue', 'value'),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date')]
)
def atualiza_grafico_pie_revenue(data_revenue, revenue, start_date, end_date):
    df = pd.DataFrame(data_revenue)
    df = df[df['Category'].isin(revenue)]

    mask = (df['Date'] > start_date) & (df['Date'] <= end_date)
    df = df.loc[mask]

    fig = px.pie(df, values=df['Value'], names=df["Category"],
                 hole=.2)
    fig.update_traces(textposition='inside',
                      textinfo='percent+label', showlegend=False)
    fig.update_layout(title={'text': "Revenue"})
    fig.update_layout(margin=graph_margin, height=300)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig

# # Gráfico 4


@app.callback(
    Output('graph4', "figure"),
    [Input('store-expenses', 'data'),
     Input('dropdown-expense', 'value'),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date')]
)
def atualiza_grafico_pie_expense(data_expense, expense,  start_date, end_date):
    df = pd.DataFrame(data_expense)
    df = df[df['Category'].isin(expense)]

    mask = (df['Date'] > start_date) & (df['Date'] <= end_date)
    df = df.loc[mask]

    fig = px.pie(df, values=df['Value'], names=df["Category"], hole=.2)
    fig.update_layout(title={'text': "Expenses"})
    fig.update_traces(textposition='inside',
                      textinfo='percent+label', showlegend=False)
    fig.update_layout(margin=graph_margin, height=300)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig
