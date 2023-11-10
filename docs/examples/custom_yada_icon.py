import dash
import dash_bootstrap_components as dbc
from dash_yada import YadaAIO

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

yada_icon = "https://user-images.githubusercontent.com/72614349/236646464-1471e596-b234-490d-bf84-e2ef7a63b233.png"
hover_message_props = {
    "name": "Hedwig",
    "greeting": "Let's explore! Just pick a tour and we'll get started",
}

yada = YadaAIO(
    yada_id="my_yada", yada_src=yada_icon, hover_message_props=hover_message_props
)

app.layout = dbc.Container(yada)


if __name__ == "__main__":
    app.run_server(debug=True)
