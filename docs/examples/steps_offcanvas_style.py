import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_yada import YadaAIO

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


steps_offcanvas_style = {
    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
    "margin": "8px auto",
    "padding": "0px 24px 5px",
    "backgroundColor": "var(--bs-gray-500)",
    "color": "white",
    "borderRadius": 12,
    "maxWidth": 800,
}


yada = YadaAIO(
    yada_id="yada",
    steps_offcanvas_style=steps_offcanvas_style,
    scripts={
        "Intro": [
            {
                "target": "#title",
                "convo": """
                ### Welcome to My Dashboard tour!  
                The tour steps are are displayed in an offcanvas component and can be styled with the `steps_offcanvas_style` prop. 
                 
                Note that you can use Markdown in the "convo" prop.
                """,
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
