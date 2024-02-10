import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context, exceptions, dash_table
from dash.dependencies import Input, Output, State
from utils import StatemantTransform
from app import app
import dash
import pandas as pd

## create a function to return the modal
def modal_import_statement(modal_id, modal_title, name_button):
    modal_import = dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(modal_title), close_button=True),
        dbc.ModalBody([
            html.Div(id='div-data-import-statement', children=[
                dbc.Select(options=[], id='select-banco'),
                dcc.Upload(id='upload-data-import-statement', contents=None, multiple=False),
            ]
                     ),
            dcc.Store(id='temporary-contents-statement', storage_type='memory'),
        ]),
        dbc.ModalFooter(
            dbc.Button(name_button, id="add-statement", className="ml-auto")
        ),
    ],
    id=modal_id,
    )
    return modal_import

## callback para se caso o dcc.Store estiver preenchido, aparece uma tabela com as transações
def callback_manage_div_upload_data(id_div_data_import_statement, id_modal_import_statement, id_store_statement, banks_options):
    @app.callback(
        Output(id_div_data_import_statement, 'children'),
        Output(id_modal_import_statement, 'size'),
        Input(id_store_statement, 'data')
    )
    def div_upload_data(data):
        if data:
            df_receitas_imported = pd.DataFrame(data['receitas'])
            df_receitas_imported['Tipo'] = 'Receita'
            df_despesas_imported = pd.DataFrame(data['despesas'])
            df_despesas_imported['Tipo'] = 'Despesa'
            df_combined = pd.concat([df_receitas_imported, df_despesas_imported])
            df_combined.fillna('-', inplace=True)    
            df_combined['Valor'] = pd.to_numeric(df_combined['Valor'], errors='coerce')
            df_combined['Valor'] = df_combined['Valor'].apply(lambda x: f'$ {x:.2f}'.replace('.', ','))
            df_combined.loc[df_combined['Efetuado'] == 0, 'Efetuado'] = 'Não'
            df_combined.loc[df_combined['Efetuado'] == 1, 'Efetuado'] = 'Sim'
            df_combined.loc[df_combined['Fixo'] == 0, 'Fixo'] = 'Não'
            df_combined.loc[df_combined['Fixo'] == 1, 'Fixo'] = 'Sim'
            df_combined['Data'].replace('-', pd.NaT, inplace=True)
            df_combined['Data'] = pd.to_datetime(df_combined['Data'], format='mixed', errors='coerce')
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
            upload = [
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Selecione o banco:"),
                        dbc.Select(
                            id="select-banco",
                            options=banks_options + [{"label": "Outro Banco", "value": "OutroBanco"}],
                            value=banks_options[0]["value"],
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
            return upload, 'md'

## Importação de extratos bancários e limpar store caso o modal seja fechado ou importado
def callback_statement_store(id_store_statement, id_modal_import_statement, id_add_statement_button, id_upload_statement, id_select_bank):
    @app.callback(
        Output(id_store_statement, 'data'),
        [
            Input(id_upload_statement, 'contents'),
            Input(id_modal_import_statement, 'is_open'),
            Input(id_add_statement_button, 'n_clicks')
        ],
        State(id_select_bank, 'value'),
    )
    def process_file(contents, modal_import_statement_is_open, add_statement_button, banco):
        ctx = callback_context
        if not ctx.triggered:
            raise exceptions.PreventUpdate
                
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if triggered_id == id_modal_import_statement and not modal_import_statement_is_open:
            return None
        elif triggered_id == id_add_statement_button and add_statement_button is not None:
            return None
        elif triggered_id == id_upload_statement and contents is not None:
            extrato = StatemantTransform(contents)
            if banco == 'Wise':
                receitas_transformed, despesas_transformed = extrato.transform_wise()
                return {'receitas': receitas_transformed.to_dict(), 'despesas': despesas_transformed.to_dict()}
            elif banco == 'CGD':
                receitas_transformed, despesas_transformed = extrato.transform_cgd()
                return {'receitas': receitas_transformed.to_dict(), 'despesas': despesas_transformed.to_dict()}
            elif banco == 'Nubank':
                receitas_transformed, despesas_transformed = extrato.transform_nubank()
                return {'receitas': receitas_transformed.to_dict(), 'despesas': despesas_transformed.to_dict()}
            elif banco == 'Inter':
                receitas_transformed, despesas_transformed = extrato.transform_inter()
                return {'receitas': receitas_transformed.to_dict(), 'despesas': despesas_transformed.to_dict()}
            elif banco == 'OutroBanco':
                ## TODO: implementar uma criação de importação de extrato bancário genérico
                return None
        return None
    return process_file