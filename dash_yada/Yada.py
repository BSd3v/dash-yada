import dash
from dash import html, Output, Input, callback, MATCH, clientside_callback, dcc, State
import uuid
import dash_bootstrap_components as dbc
import json

def addScripts():
    scripts = {}
    for pg in dash.page_registry:
        if 'addScripts' in dash.page_registry[pg]:
            scripts.update(dash.page_registry[pg]['addScripts'])
    return scripts

class Yada(html.Div):
    """A html.Div All-in-One component.


    Keyword arguments:

    - yada_id (string; optional):
        The ID used to identify this component in Dash callbacks.

    - sleepmessage_props (dict; optional):
        Props to display for the message when yada is not clicked and not playing a script.

    - activemessage_props (dict; optional):
        Props to display for the message when yada is clicked and not playing a script.

    - playscript_props (dict; optional):
        Props to control the options for the play button to run the scripts.

    - yada_src (string; optional):
        Location of the image that you want to display for yada.

    - scripts (dict; optional):
        Dictionary of keys to scripts:
            - each key will have an array of a directory:
            {target (string; required), convo (string; required), action (string; optional),
            action_args (string; optional)}

    """

    class ids:
        sleepmessage = lambda yada_id: {
            "component": "yada",
            "subcomponent": "sleepmessage",
            "yada_id": yada_id,
        }
        sleepmessage_greeting = lambda yada_id: {
            "component": "yada",
            "subcomponent": "sleepmessage_greeting",
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
            self, sleepmessage_props={}, activemessage_props={}, playscript_props={},
            yada_src=None, scripts=None, yada_id=None
    ):

        if yada_id is None:
            yada_id = str(uuid.uuid4())
        if yada_src is None:
            yada_src = '/_dash-component-suites/dash_yada/tech-support.png'

        default_greet = """
        Hello! I am Your Automated Dashboard Assistant.  
        But you can call me, Y.A.D.A!
        """

        sleepmessage_props = sleepmessage_props.copy()
        playscript_props = playscript_props.copy()
        activemessage_props = activemessage_props.copy()
        if scripts is None:
            scripts = addScripts()
        if sleepmessage_props:
            if not sleepmessage_props['name']:
                sleepmessage_props['name'] = 'yada'
            if not sleepmessage_props['greeting']:
                sleepmessage_props['greeting'] = default_greet
        else:
            sleepmessage_props['name'] = 'yada'
            sleepmessage_props['greeting'] = default_greet
        if playscript_props:
            if not playscript_props['children']:
                playscript_props['children'] = 'play selected'
        else:
            playscript_props['children'] = 'play selected'
        if activemessage_props:
            if not activemessage_props['message']:
                activemessage_props['message'] = 'What would you like to do?'
        else:
            activemessage_props['message'] = 'What would you like to do?'

        children = [
                html.Div(html.Img(id=self.ids.dummy_div(yada_id), src=yada_src, className='sleeping'), className='yada'),
                dcc.Store(id=self.ids.scripts(yada_id), data=scripts),
                dcc.Store(id=self.ids.sleepmessage_greeting(yada_id), data=sleepmessage_props['greeting']),
                dbc.Popover(
                    [
                        dbc.PopoverHeader(sleepmessage_props['name']),
                        dbc.PopoverBody(
                            dcc.Markdown(sleepmessage_props['greeting'], id=self.ids.convo(yada_id)),
                            className='btn-info yada-info'),
                    ],
                    target=self.ids.dummy_div(yada_id),
                    trigger="hover",
                    placement='bottom',
                    id=self.ids.sleepmessage(yada_id)
                ),
                dbc.Popover(
                    dbc.PopoverBody([activemessage_props['message'],
                                     dcc.Dropdown(id=self.ids.scriptChoices(yada_id)),
                                     dbc.Button(**playscript_props, id=self.ids.playScript(yada_id))]),
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
        """function (i, g) {
            if (document.querySelector(".yada").getAttribute("convo")) {
                return document.querySelector(".yada").getAttribute("convo")
            }
            return g
        }""",
        Output(ids.convo(MATCH), "children"),
        Input(ids.sleepmessage(MATCH), "is_open"),
        State(ids.sleepmessage_greeting(MATCH), "data"),
        prevent_initial_call=True
    )

    clientside_callback(
        """
        function(o, d) {
            if (!document.querySelector('.yada > img').classList.contains('sleeping')) {
                return ['hidden', window.dash_clientside.no_update]
            }
            return ['', Object.keys(d)]
        }
        """,
        Output(ids.activemessage(MATCH), 'className'),
        Output(ids.scriptChoices(MATCH), 'options'),
        Input(ids.activemessage(MATCH), 'is_open'),
        State(ids.scripts(MATCH), 'data'),
        prevent_initial_call=True
    )

    clientside_callback(
        """
        function(c, v, d) {
            if (c) {
                if (v != '') {
                    playScript(d[v])
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
        State(ids.scripts(MATCH), 'data'),
        prevent_initial_call=True
    )