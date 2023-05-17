import dash
import numpy as np
from dash import Input, Output, dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_yada import Yada

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

yada = "https://user-images.githubusercontent.com/72614349/236646464-1471e596-b234-490d-bf84-e2ef7a63b233.png"


yada = Yada(yada_id="my_yada", yada_src=yada, yada_class="testing")

app.layout = dbc.Container(
    [
        yada,
        # dbc.Row(dbc.Col(yada, width=1), justify="end"),
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
