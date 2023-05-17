import dash_ag_grid as dag
from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from yada_scripts import yada

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

app = Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
)


columnDefs = [
    {
        "field": "country",
        "checkboxSelection": True,
        "headerCheckboxSelection": True,
    },
    {"headerName": "Continent", "field": "continent"},
    {
        "headerName": "Life Expectancy",
        "field": "lifeExp",
        "type": "rightAligned",
        "valueFormatter": {"function": "d3.format('.1f')(params.value)"},
    },
    {
        "headerName": "Population",
        "field": "pop",
        "type": "rightAligned",
        "valueFormatter": {"function": "d3.format(',.0f')(params.value)"},
    },
    {
        "headerName": "GDP per Capita",
        "field": "gdpPercap",
        "type": "rightAligned",
        "valueFormatter": {"function": "d3.format('$,.1f')(params.value)"},
    },
]

grid = dag.AgGrid(
    id="grid",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    dashGridOptions={
        "rowSelection": "multiple",
        "undoRedoCellEditing": True,
        "undoRedoCellEditingLimit": 20,
    },
    columnSize="responsiveSizeToFit",
    defaultColDef={
        "resizable": True,
        "sortable": True,
        "filter": True,
        "editable": True,
        "minWidth": 120,
    },
)

title = html.Div(
    "Gap Minder Data Explorer",
    className="text-center p-3 mb-3 bg-primary text-white",
    id="title",
)
alert = dbc.Alert(
    "This is a demo of the dash-yada component. To start click on the helpdesk icon -->",
    dismissable=True,
    id="alert",
)
app.layout = dbc.Container(
    [
        yada,
        alert,
        title,
        dcc.Input(id="quick-filter-input", placeholder="filter...", className="mb-2"),
        grid,
        html.Div(id="interactivity-container"),
    ]
)


@app.callback(
    Output("interactivity-container", "children"),
    State("grid", "virtualRowData"),
    Input("grid", "selectedRows"),
    Input('grid', 'cellValueChanged')
)
def update_graphs(rows, selected, t):
    dff = df if rows is None else pd.DataFrame(rows)
    if dff.empty:
        return []
    selected = [s["country"] for s in selected] if selected else []

    colors = ["#7FDBFF" if i in selected else "#0074D9" for i in dff.country]

    graphs = []
    for column in ["pop", "lifeExp", "gdpPercap"]:
        if column in dff:
            fig = px.bar(dff, x="country", y=column, height=250)
            fig.update_traces(marker={"color": colors})
            fig.update_layout(
                margin={"t": 10, "l": 10, "r": 10},
                xaxis={"automargin": True},
                yaxis={"automargin": True, "title": {"text": column}},
            )
            graphs.append(dcc.Graph(id=column, figure=fig))
    return graphs


@app.callback(
    Output("grid", "dashGridOptions"),
    Input("quick-filter-input", "value"),
    State("grid", "dashGridOptions"),
)
def update_filter(filter_value, grid_options):
    grid_options["quickFilterText"] = filter_value
    return grid_options


if __name__ == "__main__":
    app.run_server(debug=True)
