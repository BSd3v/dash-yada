import dash

from dash import html, Dash, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from utils import yada_test

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

columnDefs = [
    {"headerName": "Row ID", "valueGetter": {"function": "params.node.id"}},
    {"field": "make"},
    {"field": "model"},
    {"field": "price"},
]

rowData = [
    {"make": "Toyota", "model": "Celica", "price": 35000},
    {"make": "Ford", "model": "Mondeo", "price": 32000},
    {"make": "Porsche", "model": "Boxster", "price": 72000},
    {"make": "BMW", "model": "M50", "price": 60000},
    {"make": "Aston Martin", "model": "DBX", "price": 190000},
]

app.layout = html.Div([
    yada_test,
    dcc.Input(id='testing_type'),
    dbc.Button(id='test_click', children='testing click'),
    dbc.Modal('test', id='modal'),
    html.Div(id='output'),
    dag.AgGrid(
        columnDefs=columnDefs,
        rowData=rowData,
        columnSize="sizeToFit",
        defaultColDef={"resizable": True, "sortable": True, "filter": True,
                       "floatingFilter": True, "editable": True},
        dashGridOptions={
            'undoRedoCellEditing': True,
            'undoRedoCellEditingLimit': 20
        },
        id="grid"
    ),
    html.Div(id="testing", style={"position":"absolute", "top":"101vh"}, children="testing")
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
    app.run(debug=False)