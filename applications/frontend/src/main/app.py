#!/usr/bin/env python3

from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server

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
    dcc.Input(id="drug-input", type="text", placeholder="Enter a drug name"),
    dbc.Button("Submit", id="submit-button", color="primary", className="mb-2", size="lg"),

    html.Div(id="output-container")
])

@app.callback(
    [Output("output-container", "children"),
     [Input("submit-button", "n_clicks")],
     [State("drug-input", "value")]]
)
def update_output(n_clicks, drug_name):
    if not drug_name:
        return ""
    
    return [f"You searched for for: {drug_name}"]
    
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)


