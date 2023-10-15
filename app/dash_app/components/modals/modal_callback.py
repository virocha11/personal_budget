from dash.dependencies import Input, Output, State
from dash import callback_context, dash
from ....app import app
from ...data_loader import data_dir, data_files
import pandas as pd
import os

## Callback to manage categories in modals ##
def callback_manege_category_modal(id):
    @app.callback(
        [
            Output(f"select_{id}", "options"),
            Output(f'checklist-selected-style-{id}', 'options'),
            Output(f'checklist-selected-style-{id}', 'value'),
            Output(f'stored-cat-{id}s', 'data')
        ],
        [
            Input(f"add-category-{id}", "n_clicks"),
            Input(f"remove-category-{id}", 'n_clicks')
        ],
        [
            State(f"input-add-{id}", "value"),
            State(f'checklist-selected-style-{id}', 'value'),
            State(f'stored-cat-{id}s', 'data')
        ]
    )
    def add_category(n, n2, txt, check_delete, data):
        categories = list(data["Categoria"].values())

        if n and not (txt == "" or txt == None):
            categories = categories + \
                [txt] if txt not in categories else categories

        if n2:
            if len(check_delete) > 0:
                categories = [i for i in categories if i not in check_delete]

        opt = [{"label": i, "value": i} for i in categories]
        df_categories = pd.DataFrame(categories, columns=['Categoria'])
        df_categories.to_csv(os.path.join(
            data_dir, data_files[f'categorias_{id}s']))
        data_return = df_categories.to_dict()

        return [opt, opt, [], data_return]
    return add_category

## Callback to open modals ##
def callback_open_modal(id_button, id_modal):
    @app.callback(
        Output(id_modal, "is_open"),
        [Input(id_button, "n_clicks")],
        [State(id_modal, "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open
    return toggle_modal

# gerenciar adicionar receitas e despesas
def calback_add_transactions(
                            id_add_statement_button, 
                            id_save_revenue_button, 
                            id_save_expense_button, 
                            id_store_statement,
                            id_description_revenue,
                            id_value_revenue,
                            id_date_revenue,
                            id_switches_revenue,
                            id_select_category_revenue,
                            id_description_expense,
                            id_value_expense,
                            id_date_expense,
                            id_switches_expense,
                            id_select_category_expense,
                            id_store_revenues,
                            id_store_expenses
                            ):
    @app.callback(
        [
            Output(id_store_revenues, 'data'),
            Output(id_store_expenses, 'data'),
        ],
        [
            Input(id_add_statement_button, 'n_clicks'),
            Input(id_save_revenue_button, 'n_clicks'),
            Input(id_save_expense_button, 'n_clicks')
        ],
        [
            State(id_store_statement, 'data'),
            State(id_description_revenue, 'value'),
            State(id_value_revenue, 'value'),
            State(id_date_revenue, 'date'),
            State(id_switches_revenue, 'value'),
            State(id_select_category_revenue, 'value'),
            State(id_description_expense, 'value'),
            State(id_value_expense, 'value'),
            State(id_date_expense, 'date'),
            State(id_switches_expense, 'value'),
            State(id_select_category_expense, 'value'),
            State(id_store_revenues, 'data'),
            State(id_store_expenses, 'data'),
        ]
    )
    def manage_add_transactions_callback(
        add_statement_button_n_clicks,
        save_revenue_button_n_clicks,
        save_expense_button_n_clicks,
        store_statement_data,
        description_revenue_value,
        revenue_value,
        date_revenue_value,
        switches_revenue_value,
        select_category_revenue_value,
        description_expense_value,
        expense_value,
        date_expense_value,
        switches_expense_value,
        select_category_expense_value,
        store_revenues_data,
        store_expenses_data
    ):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        df_revenues = pd.DataFrame(store_revenues_data)
        df_expenses = pd.DataFrame(store_expenses_data)
        
        if triggered_id == id_add_statement_button and store_statement_data != {} and add_statement_button_n_clicks is not None:
            revenues_transformed = pd.DataFrame(store_statement_data['receitas'])
            expenses_transformed = pd.DataFrame(store_statement_data['despesas'])

            df_revenues_novo = pd.concat([df_revenues, revenues_transformed])
            df_expenses_novo = pd.concat([df_expenses, expenses_transformed])

            df_revenues_novo.to_csv(os.path.join(
                data_dir, data_files['receitas']))
            df_expenses_novo.to_csv(os.path.join(
                data_dir, data_files['despesas']))
            return df_revenues_novo.to_dict(), df_expenses_novo.to_dict()
        
        elif triggered_id == id_save_revenue_button and save_revenue_button_n_clicks is not None:
            if not (revenue_value == "" or revenue_value is None):
                revenue_value = round(float(revenue_value), 2)
                date_revenue_value = pd.to_datetime(date_revenue_value).date()
                select_category_revenue_value = select_category_revenue_value[0] if type(
                    select_category_revenue_value) == list else select_category_revenue_value

                recebido = 1 if 1 in switches_revenue_value else 0
                fixo = 1 if 2 in switches_revenue_value else 0

                df_revenues.loc[df_revenues.shape[0]] = [
                    revenue_value, recebido, fixo, date_revenue_value, select_category_revenue_value, description_revenue_value]
                df_revenues.to_csv(os.path.join(
                    data_dir, data_files['receitas']))

                data_return = df_revenues.to_dict()
                return data_return, dash.no_update
        elif triggered_id == id_save_expense_button and save_expense_button_n_clicks is not None:
            if not (expense_value == "" or expense_value is None):
                expense_value = round(float(expense_value), 2)
                date_expense_value = pd.to_datetime(date_expense_value).date()
                select_category_expense_value = select_category_expense_value[0] if type(
                    select_category_expense_value) == list else select_category_expense_value

                recebido = 1 if 1 in switches_expense_value else 0
                fixo = 1 if 2 in switches_expense_value else 0

                df_expenses.loc[df_expenses.shape[0]] = [
                    expense_value, recebido, fixo, date_expense_value, select_category_expense_value, description_expense_value]
                df_expenses.to_csv(os.path.join(
                    data_dir, data_files['despesas']))

                data_return = df_expenses.to_dict()
                return dash.no_update, data_return
        else:
            return dash.no_update, dash.no_update
        
    return manage_add_transactions_callback
    
    
# @app.callback(
#     [
#         Output('store-receitas', 'data'),
#         Output('store-despesas', 'data'),
#     ],
#     [
#         Input('add-statement', 'n_clicks'),
#         Input('salvar_receita', 'n_clicks'),
#         Input('salvar_despesa', 'n_clicks')
#     ],
#     [
#         State('temporary-contents-statement', 'data'),
#         State('txt-receita', 'value'),
#         State('valor_receita', 'value'),
#         State('date-receita', 'date'),
#         State('switches-input-receita', 'value'),
#         State('select_receita', 'value'),
#         State('txt-despesa', 'value'),
#         State('valor_despesa', 'value'),
#         State('date-despesa', 'date'),
#         State('switches-input-despesa', 'value'),
#         State('select_despesa', 'value'),
#         State('store-receitas', 'data'),
#         State('store-despesas', 'data'),
#     ]
# )
# def manage_add_transactions_callback(n_clicks_add_statemant, n_clicks_receita, n_clicks_despesa, contents, descricao_receita, valor_receita, date_receita, switches_receita, categoria_receita, descricao_despesa, valor_despesa, date_despesa, switches_despesa, categoria_despesa, dict_receitas, dict_despesas):
#     ctx = callback_context
#     triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
#     df_receitas = pd.DataFrame(dict_receitas)
#     df_despesas = pd.DataFrame(dict_despesas)

#     if triggered_id == 'add-statement' and contents != {} and n_clicks_add_statemant is not None:
#         receitas_transformed = pd.DataFrame(contents['receitas'])
#         despesas_transformed = pd.DataFrame(contents['despesas'])

#         df_receitas_novo = pd.concat([df_receitas, receitas_transformed])
#         df_despesas_novo = pd.concat([df_despesas, despesas_transformed])

#         df_receitas_novo.to_csv(os.path.join(
#             data_dir, data_files['receitas']))
#         df_despesas_novo.to_csv(os.path.join(
#             data_dir, data_files['despesas']))
#         return df_receitas_novo.to_dict(), df_despesas_novo.to_dict()

#     elif triggered_id == 'salvar_receita' and n_clicks_receita is not None:
#         if n_clicks_receita and not (valor_receita == "" or valor_receita is None):
#             valor_receita = round(float(valor_receita), 2)
#             date_receita = pd.to_datetime(date_receita).date()
#             categoria_receita = categoria_receita[0] if type(
#                 categoria_receita) == list else categoria_receita

#             recebido = 1 if 1 in switches_receita else 0
#             fixo = 1 if 2 in switches_receita else 0

#             df_receitas.loc[df_receitas.shape[0]] = [
#                 valor_receita, recebido, fixo, date_receita, categoria_receita, descricao_receita]
#             df_receitas.to_csv(os.path.join(
#                 data_dir, data_files['receitas']))

#             data_return = df_receitas.to_dict()
#             return data_return, dash.no_update

#     elif triggered_id == 'salvar_despesa' and n_clicks_despesa is not None:
#         if n_clicks_despesa and not (valor_despesa == "" or valor_despesa is None):
#             valor_despesa = round(float(valor_despesa), 2)
#             date_despesa = pd.to_datetime(date_despesa).date()
#             categoria_despesa = categoria_despesa[0] if type(
#                 categoria_despesa) == list else categoria_despesa

#             recebido = 1 if 1 in switches_despesa else 0
#             fixo = 1 if 2 in switches_despesa else 0

#             df_despesas.loc[df_despesas.shape[0]] = [
#                 valor_despesa, recebido, fixo, date_despesa, categoria_despesa, descricao_despesa]
#             df_despesas.to_csv(os.path.join(
#                 data_dir, data_files['despesas']))

#             data_return = df_despesas.to_dict()

#         return dash.no_update, df_despesas.to_dict()

#     return dash.no_update, dash.no_update
