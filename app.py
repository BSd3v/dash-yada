import dash
from dash_yada import Yada
from dash import html, Dash, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

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
    Yada(yada_id='test',
         sleep_message_props={'greeting':'''
         _rawr!_  \r
          check out:  \r
          * 1  \r
          * 2  \r
          [markdown](#)
          '''},
         active_message="testing",
         play_script_props={'color':'warning', 'children': 'play'},
         scripts={'explore': [
                {'target': '#testing_type', 'convo':'I can interact with input boxes',
                               'action': 'type', 'action_args': 'test'},
                {'target': '#test_click', 'convo':'and click buttons', 'action': 'click'},
             {'target': '#modal', 'convo': 'I can go onto modals'},
                {'target': '#grid', "convo": "I can highlight entire elements"},
                {'target': '#grid .ag-header-cell .ag-header-cell-label',
                 "convo": "I can sort grids", "action": "click"},
                {'target': '#grid .ag-header-cell:nth-child(3) .ag-header-cell-label',
                 "convo": "I can multi-sort grids", "action": "click", "action_args": {"shiftKey": True}},
             {'target': '.ag-row[row-index="2"] .ag-cell[aria-colindex="3"]', "action": "dblclick", "convo": "I can edit a grid"},
             {'target': '.ag-row[row-index="2"] .ag-cell[aria-colindex="3"] input',
              "action": "type", "convo": "I can edit a grid", "action_args": "testing"},
            {'target': '.ag-row[row-index="1"] .ag-cell[aria-colindex="3"]',
              "action": "click", "convo": "See?"},
            {'target': '.ag-row[row-index="1"] .ag-cell[aria-colindex="3"]', "convo": "I can even ctrl-z",
             "action": "sendKeys", "action_args": {"ctrlKey": True, "key": "z", "code": "KeyZ", "keyCode": 90}},
                {'target': '#grid .ag-header-row-column-filter .ag-header-cell:nth-child(2)'
                           ' .ag-input-wrapper .ag-input-field-input',
                 "convo": "I filter as well", "action": "type", "action_args": "BMW"},
             {'target': "#grid .ag-header-cell:nth-child(2)", "convo": 'See!  \rI just applied a filter to this column'},
             {'target': "#testing", "convo": "I can even scroll"}
            ]},
         next_button_props={'size':'sm', 'class_name': 'fa-solid fa-arrow-right mb-2', 'children': ''},
        prev_button_props={'size':'sm', 'class_name': 'fa-solid fa-arrow-left mb-2', 'children': ''}
         ),
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
    app.run(debug=True)