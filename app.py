import dash
from dash_yada import Yada
from dash import html, Dash, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

app = Dash(__name__, use_pages=True, pages_folder='', external_stylesheets=[dbc.themes.BOOTSTRAP])

dash.register_page('home', path='/', layout=html.Div('rawr'))

app.layout = html.Div([
    Yada(yada_id='test',
         sleep_message_props={'greeting':[dcc.Markdown('''
         _rawr!_  
          check out:  
          * 1  
          * 2  
          [markdown](#)
          ''')]},
         active_message="testing",
         play_script_props={'color':'warning', 'children': 'play'},
         scripts={'explore': [{'target': '#testing_type', 'convo':'testing', 'action': 'send_keys', 'action_args': 'test'},
                              {'target': '#test_click', 'convo':'rawr',
                               'action': 'click'}]}
         ),
    dcc.Input(id='testing_type'),
    dbc.Button(id='test_click', children='testing click'),
    dbc.Modal('test', id='modal'),
    html.Div(id='output'),
    dash.page_container
])

@app.callback(
    Output('modal', 'is_open'),
    Input('test_click', 'n_clicks')
)
def show(n):
    if n:
        return True

@app.callback(
    Output('output', 'children'),
    Input('testing_type', 'value')
)
def typing(v):
    return v

if __name__ == '__main__':
    app.run(debug=True)