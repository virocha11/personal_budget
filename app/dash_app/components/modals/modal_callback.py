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
