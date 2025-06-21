def init_dash_app(server):
    from dash import Dash, dcc, html, Input, Output, State
    import dash_bootstrap_components as dbc
    from applications.data_analyzer.src.main.data_analyzer import get_top_drugs
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

    app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.COSMO])


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
            options=[],
            placeholder="Select a drug",
            #style={"width": "50%", "margin-bottom": 20px}
        ),

        html.Div(id="output-container")
    ])

    @app.callback(
            Output("drug-dropdown", "options"),
            Input("drug-dropdown", "id"),
            prevent_initial_call=False
    )
    def populate_dropdown(_):
        try:
            drug_names = get_top_drugs(50)
            return [{"label": drug.title(), "value": drug} for drug in drug_names]

        except Exception as e:
            logging.error(f"Failed to fetch top drugs: {e}")
            return []

    return app