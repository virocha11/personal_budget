import pandas as pd
import os

path_data_files = 'data'
data_files = {
    'revenues': "df_revenues.csv",
    'expenses': "df_expenses.csv",
    'categories_revenues': "df_cat_revenues.csv",
    'categories_expenses': "df_cat_expenses.csv",
}

if (data_files['expenses'] in os.listdir(path_data_files)) and (data_files['revenues'] in os.listdir(path_data_files)):
    df_expenses = pd.read_csv(os.path.join(
        path_data_files, data_files['expenses']), index_col=0, parse_dates=True)
    df_revenues = pd.read_csv(os.path.join(
        path_data_files, data_files['revenues']), index_col=0, parse_dates=True)
    df_revenues["Date"] = pd.to_datetime(df_revenues["Date"])
    df_revenues["Date"] = df_revenues["Date"].apply(lambda x: x.date())
    df_expenses["Date"] = pd.to_datetime(df_expenses["Date"])
    df_expenses["Date"] = df_expenses["Date"].apply(lambda x: x.date())

else:
    data_structure = {'Valor': [],
                      'Efetuado': [],
                      'Fixo': [],
                      'Date': [],
                      'Categoria': [],
                      'Descrição': [], }

    df_revenues = pd.DataFrame(data_structure)
    df_expenses = pd.DataFrame(data_structure)
    df_expenses.to_csv(os.path.join(path_data_files, data_files['expenses']))
    df_revenues.to_csv(os.path.join(path_data_files, data_files['revenues']))

if (data_files['categories_revenues'] in os.listdir(path_data_files)) and (data_files['categories_expenses'] in os.listdir(path_data_files)):
    df_cat_revenue = pd.read_csv(os.path.join(
        path_data_files, data_files['categories_revenues']), index_col=0)
    df_cat_expense = pd.read_csv(os.path.join(
        path_data_files, data_files['categories_expenses']), index_col=0)
    cat_revenue = df_cat_revenue.values.tolist()
    cat_expense = df_cat_expense.values.tolist()

else:
    cat_revenue = {'Categoria': ["Salary", "Investments", "Comissions"]}
    cat_expense = {'Categoria': ["Food",
                                 "Rent", "Gasoline", "Health", "Entreteriment", "Education", "Others"]}

    df_cat_revenue = pd.DataFrame(cat_revenue, columns=['Categoria'])
    df_cat_expense = pd.DataFrame(cat_expense, columns=['Categoria'])
    df_cat_revenue.to_csv(os.path.join(
        path_data_files, data_files['categories_revenues']))
    df_cat_expense.to_csv(os.path.join(
        path_data_files, data_files['categories_expenses']))
