import dash
from dash_yada import Yada
from dash import html, Dash, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, pages_folder='', external_stylesheets=[dbc.themes.BOOTSTRAP])

dash.register_page('home', path='/', addScripts={'explore': [{'target': '#_pages_content', 'convo':'testing'},
                                                             {'target': '.yada', 'convo':'rawr'}]},
                   layout=html.Div('rawr'))

app.layout = html.Div([
    Yada(yada_id='test'),
    dash.page_container,
])

if __name__ == '__main__':
    app.run(debug=True)