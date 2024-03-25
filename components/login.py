from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import supabase_py as supabase

from app import app

from configparser import ConfigParser
config = ConfigParser()
config.read('static/config/config.ini')
url: str = config.get('supabase','url')
key: str = config.get('supabase','key')

supabase_client = supabase.create_client(url, key)

def is_authenticated():
    # Aqui você pode adicionar a lógica para verificar se o usuário está autenticado
    # Por enquanto, vamos retornar True para fins de exemplo    
    user = supabase_client.auth.user()
    if user is not None:
        return True
    else:
        return False

# Layout da página de login
login_layout = dbc.Container(
    [
                html.Div([
                    html.H1("Personal Budget",
                            className="display-5 text-primary fw-bolder mt-3"),
                    html.P("By Vitor Rocha", className="text-muted fs-6"),
                    html.Hr(className="my-3")
                ], style={"text-align": "center"}),
                dbc.Input(id="login-email", type="text", placeholder="Username"),
                dbc.Input(id="login-password", type="password", placeholder="Password", className="mt-2"),
                dbc.Button("Login", id="login-button", color="primary", className="mt-3"),
                html.Div(id="login-alert", className="mt-3"),
                # local para o botão de registro
                html.Div([
                    html.P("Don't have an account?"),
                    dbc.Button("Register", id="register-link", color="link", className="mt-3")
                ], style={"text-align": "center"}),
                # Layout da página de registro
                dbc.Modal(
                    [
                        dbc.ModalHeader("Create Account"),
                        dbc.ModalBody(
                            [
                                dbc.Input(id="register-email", type="email", placeholder="Email", className="mt-2"),
                                dbc.Input(id="register-password", type="password", placeholder="Password", className="mt-2"),
                                dbc.Button("Register", id="register-button", color="primary", className="mt-3"),
                                html.Div(id="register-alert", className="mt-3"),
                            ]
                        ),
                    ],
                    id="register-modal",
                    style={"background-color": "rgba(17, 140, 79, 0.05)"},
                    size="lg",
                    is_open=False,
                    centered=True,
                ),
    ],
    className="mt-5",
    style={"max-width": "500px"}
)

# Callback para fazer login
@app.callback(
    [Output("login-alert", "children"),
     Output("redirect-trigger", "data")],
    [Input("login-button", "n_clicks")],
    [State("login-email", "value"), State("login-password", "value")]
)
def login(n_clicks, login_email, login_password):
    if n_clicks:
        response = supabase_client.auth.sign_in(email=login_email, password=login_password)
        if response["status_code"] == 200:
            text_success: str = "Login successful. Redirecting..."
            print(response)
            return html.Div(text_success, style={"color": "green", "margin-top": "10px", "margin-bottom": "10px"}), True
        else:
            text_error: str = "Invalid username or password. Please try again."
            print(response)
            return html.Div(text_error, style={"color": "red", "margin-top": "10px", "margin-bottom": "10px"}), False
    else:
        raise PreventUpdate
    
# Callback para registrar um novo usuário
@app.callback(
    Output("register-modal", "is_open"),
    [Input("register-link", "n_clicks")],
    [State("register-modal", "is_open")],
)
def register_modal(n_register_clicks, is_open):
    if n_register_clicks:
        return not is_open
    return is_open

# Callback para fazer o registro
@app.callback(
    Output("register-alert", "children"),
    [Input("register-button", "n_clicks"), Input("register-password", "n_key_press")],
    [State("register-email", "value"), State("register-password", "value")],
)
def register(n_clicks, n_key_press, email, password):
    ctx = callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"]
        if prop_id == "register-button.n_clicks" or (prop_id == "register-password.n_key_press" and n_key_press == 13):
            if n_clicks:
                response = supabase_client.auth.sign_up(email=email, password=password)
                if response["status_code"] == 200:
                    print(response)
                    # Registro bem-sucedido
                    text_success: str = "Registration successful. Please check your email to verify your account."
                    return html.Div(text_success, style={"color": "green", "margin-top": "10px", "margin-bottom": "10px"})
                else:
                    print(response)
                    # Falha no registro
                    text_error: str = "Failed to register. Please try again."
                    return html.Div(text_error, style={"color": "red", "margin-top": "10px", "margin-bottom": "10px"})
            else:
                raise PreventUpdate
