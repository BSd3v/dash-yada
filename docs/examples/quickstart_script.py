import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_yada import YadaAIO

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

yada = YadaAIO(
    yada_id="yada",
    scripts={
        "Intro": [
            {
                "target": "#title",
                "convo": "Welcome to My Dashboard tour!",
            },
        ]
    },
)


app.layout = dbc.Container(
    [
        yada,
        html.H4(
            "My Dashboard",
            className="p-3 bg-primary text-white text center",
            id="title",
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
