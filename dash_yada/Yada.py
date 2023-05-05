import dash
from dash import html, Output, Input, callback, MATCH, clientside_callback, dcc, State
import uuid
import dash_bootstrap_components as dbc

def addScripts():
    scripts = {}
    for pg in dash.page_registry:
        if 'addScripts' in dash.page_registry[pg]:
            scripts[dash.page_registry[pg]['path']] = dash.page_registry[pg]['addScripts']
    return scripts

class Yada(html.Div):
    class ids:
        sleepmessage = lambda yada_id: {
            "component": "yada",
            "subcomponent": "sleepmessage",
            "yada_id": yada_id,
        }
        convo = lambda yada_id: {
            "component": "yada",
            "subcomponent": "convo",
            "yada_id": yada_id,
        }
        activemessage = lambda yada_id: {
            "component": "yada",
            "subcomponent": "activemessage",
            "yada_id": yada_id,
        }
        scripts = lambda yada_id: {
            "component": "yada",
            "subcomponent": "scripts",
            "yada_id": yada_id,
        }
        scriptChoices = lambda yada_id: {
            "component": "yada",
            "subcomponent": "scriptChoices",
            "yada_id": yada_id,
        }
        dummy_div = lambda yada_id: {
            "component": "yada",
            "subcomponent": "dummy_div",
            "yada_id": yada_id,
        }
        playScript = lambda yada_id: {
            "component": "yada",
            "subcomponent": "playScript",
            "yada_id": yada_id,
        }

    ids = ids
    def __init__(
            self, sleepmessage_props={}, activemessage_props={}, scriptmessage_props={}, playscript_props={},
            yada_src=None, scripts=None, yada_id=None
    ):
        args = {}
        """

        """

        if yada_id is None:
            yada_id = str(uuid.uuid4())
        if yada_src is None:
            yada_src = '/_dash-component-suites/dash_yada/tech-support.png'

        sleepmessage_props = sleepmessage_props.copy()
        playscript_props = playscript_props.copy()
        activemessage_props = activemessage_props.copy()
        scriptmessage_props = scriptmessage_props.copy()
        if scripts is None:
            scripts = addScripts()

        children = [
                html.Div(html.Img(id=self.ids.dummy_div(yada_id), src=yada_src, className='sleeping'), className='yada'),
                dcc.Store(id=self.ids.scripts(yada_id), data=scripts),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("yada"),
                        dbc.PopoverBody(
                            "Hello!\nI am Your Automated Dashboard Assistant.\nBut you can call me Yada!",
                            className='btn-info', id=self.ids.convo(yada_id)),
                    ],
                    target=self.ids.dummy_div(yada_id),
                    trigger="hover",
                    placement='bottom',
                    id=self.ids.sleepmessage(yada_id)
                ),
                dbc.Popover(
                    dbc.PopoverBody(['What do you want to do?',
                                     dcc.Dropdown(id=self.ids.scriptChoices(yada_id)),
                                     dbc.Button(id=self.ids.playScript(yada_id), children=['Play'])]),
                    target=self.ids.dummy_div(yada_id),
                    trigger="legacy",
                    placement='left',
                    id=self.ids.activemessage(yada_id)
                ),
            ]

        super(Yada, self).__init__(children)

    clientside_callback(
        """
        async function (n, o) {
            if (document.querySelector('.yada > img').classList.contains('sleeping')) {
                return !o
            }
            return window.dash_clientside.no_update
        }
        """,
        Output(ids.sleepmessage(MATCH), "is_open"),
        Input(ids.dummy_div(MATCH), 'n_clicks'),
        State(ids.scriptChoices(MATCH), 'is_open'),
        prevent_initial_call=True
    )

    clientside_callback(
        """function (is) {
            if (document.querySelector(".yada").getAttribute("convo")) {
                return document.querySelector(".yada").getAttribute("convo")
            }
            return "Hello! I am Your Automated Dashboard Assistant. But you can call me Yada!"
        }""",
        Output(ids.convo(MATCH), "children"),
        Input(ids.sleepmessage(MATCH), "is_open"),
        prevent_initial_call=True
    )

    clientside_callback(
        """
        function(o, p, d) {
            if (!document.querySelector('.yada > img').classList.contains('sleeping')) {
                return ['hidden', window.dash_clientside.no_update]
            }
            return ['', Object.keys(d[p])]
        }
        """,
        Output(ids.activemessage(MATCH), 'className'),
        Output(ids.scriptChoices(MATCH), 'options'),
        Input(ids.activemessage(MATCH), 'is_open'),
        State('_pages_location', 'pathname'),
        State(ids.scripts(MATCH), 'data'),
        prevent_initial_call=True
    )

    clientside_callback(
        """
        function(c, v, p, d) {
            if (c) {
                if (v != '') {
                    playScript(d[p][v])
                    return [false, '']
                }
            }
            return [true, '']
        }
        """,
        Output(ids.activemessage(MATCH), 'is_open'),
        Output(ids.convo(MATCH), "children", allow_duplicate=True),
        Input(ids.playScript(MATCH), 'n_clicks'),
        State(ids.scriptChoices(MATCH), 'value'),
        State('_pages_location', 'pathname'),
        State(ids.scripts(MATCH), 'data'),
        prevent_initial_call=True
    )