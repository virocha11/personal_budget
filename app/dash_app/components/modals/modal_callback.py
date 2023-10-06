from dash.dependencies import Input, Output, State
from ....app import app
from ...data_loader import data_dir, data_files
import pandas as pd
import os

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

def callback_open_modal(id):
    @app.callback(
        Output(f"modal-new-{id}", "is_open"),
        [Input(f"new-{id}", "n_clicks")],
        [State(f"modal-new-{id}", "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open
    return toggle_modal

