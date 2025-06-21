def init_dash_app(server):
    from dash import Dash, dcc, html, Input, Output, State
    import dash_bootstrap_components as dbc
    from applications.data_analyzer.src.main.data_analyzer import get_top_drugs, get_top_reactions_by_age, get_age_distribution_for_drug
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

        # Visualizations
        dcc.Graph(id="age-chart")
        dcc.Graph(id="reaction-chart")

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
        

    @app.callback(
        Output("age-chart", "figure"),
        Output("reaction-chart", "figure"),
        Input("drug-dropdown", "value")
    )
    def update_visuals(drug_name):
        if not drug_name:
            raise dash.exceptions.PreventUpdate
        
        age_data = get_age_distribution_for_drug(drug_name)
        reaction_data = get_top_reactions_by_age(drug_name)

        # Fallback
        if not age_data or not reaction_data:
            return px.bar(title="No data available"), px.bar(title="No data available")

        df_age = pd.DataFrame(age_data)
        df_reactions = pd.DataFrame([
            {"age_group": key, "reaction": val["reaction"], "count": val["count"]}
            for key, val in reaction_data.items()
        ])

        fig1 = px.bar(df_age, x="age_group", y="count", title="Age Distribution of Reports")
        fig2 = px.bar(df_reactions, x="age_group", y="count", color="reaction", title="Top Reactions by Age Group")

        return fig1, fig2

    return app