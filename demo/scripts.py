import dash
import numpy as np
from dash import Input, Output, dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_yada import Yada

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

formual_intro = dcc.Markdown(
    """
The Poisson distribution describes the probability of obtaining k successes during a given time interval.  
If a random variable X follows a Poisson distribution, then the probability that X = k successes can be found by the following formula:
"""
)
forumula = dcc.Markdown(
    "$P\\left( x \\right) = \\frac{{e^{ - \\lambda } \\lambda ^x }}{{x!}}$",
    mathjax=True,
    style={"font-size": "28pt"},
)

yada = Yada(
    yada_id="my_yada",
    yada_class="testing",
    script_message={"message": "testing"},
    play_script_props={"color": "warning", "children": "play"},
    scripts={
        "explore": [
            {
                "target": "#title",
                "convo": [html.Div([formual_intro, forumula])]
                # "convo": "This is the title"
            },
            {
                "target": "#lambda",
                # "convo":[html.Div(formual_intro, forumula)]
                "convo": "This is the title",
            },
        ]
    },
)

inputs = dbc.Card(
    [
        html.Label("lambda (must be >= 0): "),
        dcc.Input(id="lambda", placeholder="number", value=4),
    ],
    body=True,
)


graph = dbc.Card(dbc.CardBody(dcc.Graph(id="histogram")))

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(yada, width=1), justify="end"),
        html.H1("Poisson distribution graph", className="m-4", id="title"),
        inputs,
        graph,
    ],
    fluid=True,
)


@app.callback(
    Output("histogram", "figure"),
    Input("lambda", "value"),
)
def graph_histogram(lambda_value):
    if lambda_value:
        s = np.random.poisson(int(lambda_value), 10000)
        fig = px.histogram(x=s, nbins=24, histnorm="probability")
        return fig
    else:
        return dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True, port=1234)
