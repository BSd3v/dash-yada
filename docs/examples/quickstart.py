import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_yada import Yada

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        Yada(yada_id="yada"),
        html.H4("My Dashboard", className="p-3 bg-primary text-white text center"),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
