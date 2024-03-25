from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import supabase_py as supabase
from app import app
from components import despesas, sidebar, dashboards, receitas, login
from data.tables import Access_user, Access_category, Access_account, Access_account_type, Access_company, Access_product, Access_transaction, Access_transaction_type
import supabase_py as supabase

# Layout principal
app.layout = html.Div([ 
    dcc.Location(id="url"), 
    html.Div(id="main-content"),
    dcc.Store(id="redirect-trigger")
])

# Callback para renderizar o conteúdo principal
@app.callback(
    Output("main-content", "children"),
    [Input("url", "pathname"), Input("redirect-trigger", "data")]
)
def render_main_content(pathname, redirect_trigger):
    # Verificar se o usuário está autenticado
    if not login.is_authenticated():
        return login.login_layout
    
    # Se estiver autenticado, renderizar o sidebar e o conteúdo da página
    main_layout = dbc.Container(children=[
        # criação de caixinhas de memória para manipular os dados do dataframe
        # new_transaction = Access_transaction()
        # df_revenues = new_transaction.retrieve('transaction', 'transaction_type_id', '1' )
        # df_revenues["transaction_date"] = pd.to_datetime(df_revenues["transaction_date"])
        # df_revenues["transaction_date"] = df_revenues["transaction_date"].apply(lambda x: x.date())
        # df_revenues_aux = df_revenues.to_dict()

        # new_transaction = Access_transaction()
        # df_expenses = new_transaction.retrieve('transaction', 'transaction_type_id', '2')
        # df_expenses["transaction_date"] = pd.to_datetime(df_expenses["transaction_date"])
        # df_expenses["transaction_date"] = df_expenses["transaction_date"].apply(lambda x: x.date())
        # df_expenses_aux = df_expenses.to_dict()

        # new_transaction_type = Access_transaction_type()
        # df_transaction_type = new_transaction.retrieve('transactionType')

        # new_product = Access_product()
        # df_product = new_product.retrieve('product')

        # new_company = Access_company()
        # df_company = new_company.retrieve('company')

        # new_category = Access_category()
        # df_category = new_category.retrieve('category')
        # df_category_expenses = df_category[df_category['category_type_id'] == 2]
        # df_category_revenues = df_category[df_category['category_type_id'] == 1]
        # list_category_expenses = df_category_expenses.values.tolist()
        # list_category_expenses = sorted(list_category_expenses, key=lambda x: x[0])
        # list_category_revenues = df_category_revenues.values.tolist()
        # list_category_revenues = sorted(list_category_revenues, key=lambda x: x[0])

        # new_account_type = Access_account_type()
        # df_account_type = new_account_type.retrieve('accountType')

        # new_account = Access_account()
        # df_account = new_account.retrieve('account')
        
        dcc.Store(id='store-receitas', data={}),
        dcc.Store(id="store-despesas", data={}),
        dcc.Store(id='stored-cat-receitas', data={}),
        dcc.Store(id='stored-cat-despesas', data={}),

        dbc.Row([
            dbc.Col([
                dcc.Location(id="url-page"),
                sidebar.layout
            ], md=2, className="sticky-sidebar"),
            dbc.Col([
                html.Div(id="page-content")
            ], md=10, className='px-2')
        ])
    ], fluid=True,)
    return main_layout

# Callback para renderizar o conteúdo da página
@app.callback(
    Output("page-content", "children"),
    [Input("url-page", "pathname")]
)
def render_page_content(pathname):
    if pathname in ["/", "/dashboards"]:
        return dashboards.layout
    elif pathname == "/analisar-despesas":
        return despesas.layout
    elif pathname == "/analisar-receitas":
        return receitas.layout
    else:
        return "404 - Page not found"

if __name__ == '__main__':
    app.run_server(debug=True)
