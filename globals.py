import pandas as pd
import os

path_data_files = 'data'
data_files = {
    'receitas': "df_receitas.csv",
    'despesas': "df_despesas.csv",
    'categorias_receitas': "df_cat_receita.csv",
    'categorias_despesas': "df_cat_despesa.csv",
}

if (data_files['despesas'] in os.listdir(path_data_files)) and (data_files['receitas'] in os.listdir(path_data_files)):
    df_despesas = pd.read_csv(os.path.join(
        path_data_files, data_files['despesas']), index_col=0, parse_dates=True)
    df_receitas = pd.read_csv(os.path.join(
        path_data_files, data_files['receitas']), index_col=0, parse_dates=True)
    df_receitas["Date"] = pd.to_datetime(df_receitas["Date"])
    df_receitas["Date"] = df_receitas["Date"].apply(lambda x: x.date())
    df_despesas["Date"] = pd.to_datetime(df_despesas["Date"])
    df_despesas["Date"] = df_despesas["Date"].apply(lambda x: x.date())

else:
    data_structure = {'Valor': [],
                      'Efetuado': [],
                      'Fixo': [],
                      'Date': [],
                      'Categoria': [],
                      'Descrição': [], }

    df_receitas = pd.DataFrame(data_structure)
    df_despesas = pd.DataFrame(data_structure)
    df_despesas.to_csv(os.path.join(path_data_files, data_files['despesas']))
    df_receitas.to_csv(os.path.join(path_data_files, data_files['receitas']))

if (data_files['categorias_receitas'] in os.listdir(path_data_files)) and (data_files['categorias_despesas'] in os.listdir(path_data_files)):
    df_cat_receita = pd.read_csv(os.path.join(
        path_data_files, data_files['categorias_receitas']), index_col=0)
    df_cat_despesa = pd.read_csv(os.path.join(
        path_data_files, data_files['categorias_despesas']), index_col=0)
    cat_receita = df_cat_receita.values.tolist()
    cat_despesa = df_cat_despesa.values.tolist()

else:
    cat_receita = {'Categoria': ["Salário", "Investimentos", "Comissão"]}
    cat_despesa = {'Categoria': ["Alimentação",
                                 "Aluguel", "Gasolina", "Saúde", "Lazer"]}

    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_receita.to_csv(os.path.join(
        path_data_files, data_files['categorias_receitas']))
    df_cat_despesa.to_csv(os.path.join(
        path_data_files, data_files['categorias_despesas']))
