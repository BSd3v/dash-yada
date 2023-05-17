import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_yada import Yada

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

yada = Yada(yada_id="my_yada")

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(yada, width=1), justify="end"),
        html.H1("My Dashboard", className="m-4"),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
