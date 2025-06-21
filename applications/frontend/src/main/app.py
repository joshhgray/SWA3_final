def init_dash_app(server):
    from dash import Dash, dcc, html, Input, Output, State
    import dash_bootstrap_components as dbc
    from dotenv import load_dotenv
    import plotly.express as px
    import pandas as pd
    import logging
    import requests
    import dash
    import os

    logging.basicConfig(level=logging.INFO)

    # Set BACKEND_API based on debugging mode
    load_dotenv()
    TESTING = os.getenv("TESTING", "false").lower() == "true"
    if TESTING:
        BACKEND_API = "http://127.0.0.1:5050"
    else: 
        BACKEND_API = os.getenv("BACKEND_API", "https://swa-5ae147d163b6.herokuapp.com/")
    logging.info(f"Using BACKEND_API = {BACKEND_API}")

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
    server = app.server

    # utility function to fetch top n(default 50) drugs
    def fetch_top_drugs(limit=50):
        try:
            res = requests.get(f"{BACKEND_API}/drugs?limit={limit}")
            if res.status_code == 200:
                drug_names = res.json().get("drugs", [])
                return [{"label": drug_name.title(), "value": drug_name} for drug_name in drug_names]
            else:
                print(f"Error fetching drugs: {res.status_code}")
                return []

        except Exception as e:
            print(f"Error fetching drugs: {e}")
            return []
        
    drug_options = fetch_top_drugs()

    medical_disclaimer = html.Div(
        [
            dbc.Alert([
                html.B("This application is for educational and demonstration purposes only. "),
                "This application is for educational and demonstration purposes only. " \
                " The data displayed is sourced from the openFDA public API and reflects " \
                "real-world adverse event reports, but does NOT establish causation between " \
                "any drug and reported outcomes.",
                html.B(" Please note: This is NOT a medical tool "),
                "- Do not use this application to make " \
                "health-related decisions. For medical advice, diagnosis, or treatment, " \
                "please consult a qualified healthcare professional."
            ])
        
        ]
    )

    app.layout = dbc.Container([
        # Header
        dbc.Row([medical_disclaimer]),
        html.H1("FDA adverse events explorer"),

        # Body
        dcc.Dropdown(
            id="drug-dropdown",
            options=drug_options,
            placeholder="Select a drug",
            #style={"width": "50%", "margin-bottom": 20px}
        ),

        html.Div(id="output-container")
    ])

    @app.callback(
        Output("output-container", "children"),
        Input("drug-dropdown", "value"),
        prevent_initial_call=True
    )
    def update_output(drug_name):
        if not drug_name:
            return ""
        
        return f"You selected: {drug_name}"

    return app