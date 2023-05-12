import dash
from dash import html, Output, Input, callback, MATCH, clientside_callback, dcc, State
import uuid
import dash_bootstrap_components as dbc
import json


def addScripts():
    scripts = {}
    for pg in dash.page_registry:
        if "addScripts" in dash.page_registry[pg]:
            scripts.update(dash.page_registry[pg]["addScripts"])
    return scripts


class Yada(html.Div):
    """A html.Div All-in-One component.


    Keyword arguments:

    - yada_id (string; optional):
        The ID used to identify this component in Dash callbacks.

    - sleep_message_props (dict; optional):
        Props to display for the message when yada is not clicked and not playing a script.
        If not defined, the default name is "yada".  Set name to "" to not display a header.  Set message to "" to not display a greeting
        If greeting or name is a component, it must be wrapped in [ ], for example {"greeting": [html.Div("Hi")]
        {name (string; optional), greeting (string; optional)}

    - active_message (string; optional):
        String to display for the message when yada is clicked and not playing a script.

    - play_script_props (dict; optional):
        Props to control the options for the play button to run the scripts. dbc.Button props.

    - yada_src (string; optional):
        Location src of the image that you want to display for yada.

    - scripts (dict of list of dicts; optional):
        Dictionary of keys to scripts:
            - each key will have an array of a directory:
            {target (string; required), convo (string; required), action (string; optional),
            action_args (string; optional)}

    - next_button_props (dict; optional):
        Props to control the options for the next button. dbc.Button props.

    - prev_button_props (dict; optional):
        Props to control the options for the previous button. dbc.Button props.

    """

    class ids:
        sleep_message = lambda yada_id: {
            "component": "yada",
            "subcomponent": "sleep_message",
            "yada_id": yada_id,
        }
        sleep_message_greeting = lambda yada_id: {
            "component": "yada",
            "subcomponent": "sleep_message_greeting",
            "yada_id": yada_id,
        }
        convo = lambda yada_id: {
            "component": "yada",
            "subcomponent": "convo",
            "yada_id": yada_id,
        }
        active_message = lambda yada_id: {
            "component": "yada",
            "subcomponent": "active_message",
            "yada_id": yada_id,
        }
        active_body = lambda yada_id: {
            "component": "yada",
            "subcomponent": "active_body",
            "yada_id": yada_id,
        }
        scripts = lambda yada_id: {
            "component": "yada",
            "subcomponent": "scripts",
            "yada_id": yada_id,
        }
        script_choices = lambda yada_id: {
            "component": "yada",
            "subcomponent": "script_choices",
            "yada_id": yada_id,
        }
        dummy_div = lambda yada_id: {
            "component": "yada",
            "subcomponent": "dummy_div",
            "yada_id": yada_id,
        }
        sleepy_div = lambda yada_id: {
            "component": "yada",
            "subcomponent": "sleepy_div",
            "yada_id": yada_id,
        }
        play_script = lambda yada_id: {
            "component": "yada",
            "subcomponent": "play_script",
            "yada_id": yada_id,
        }

    ids = ids

    def __init__(
        self,
        sleep_message_props={},
        active_message='',
        play_script_props={},
        yada_src=None,
        scripts=None,
        yada_id=None,
        yada_class='',
        prev_button_props={},
        next_button_props={}
    ):

        if yada_id is None:
            yada_id = str(uuid.uuid4())
        if yada_src is None:
            yada_src = "/_dash-component-suites/dash_yada/tech-support.png"

        default_greet = """
        Hello! I am Your Automated Dashboard Assistant.  
        But you can call me, Y.A.D.A!
        """

        sleep_message_props = sleep_message_props.copy()
        play_script_props = play_script_props.copy()
        prev_button_props = prev_button_props.copy()
        next_button_props = next_button_props.copy()
        if scripts is None:
            scripts = addScripts()
        if sleep_message_props:
            if sleep_message_props.get("name") is None:
                sleep_message_props["name"] = "yada"
            if sleep_message_props.get("greeting") is None:
                sleep_message_props["greeting"] = default_greet
        else:
            sleep_message_props["name"] = "yada"
            sleep_message_props["greeting"] = default_greet
        if play_script_props:
            if sleep_message_props.get("children") is None:
                play_script_props["children"] = "play selected"
        else:
            play_script_props["children"] = "play selected"
        if active_message == '':
            active_message = "What would you like to do?"
            
            
        if next_button_props.get('children') is None:
            next_button_props['children'] = 'next'
        if next_button_props.get('class_name') is None:
            next_button_props['class_name'] = 'next'
        else:
            next_button_props['class_name'] = 'next ' + next_button_props['class_name']
        if next_button_props.get('style') is None:
            next_button_props['style'] = {'float': 'right'}
            
        if prev_button_props.get('children') is None:
            prev_button_props['children'] = 'previous'
        if prev_button_props.get('class_name') is None:
            prev_button_props['class_name'] = 'previous'
        else:
            prev_button_props['class_name'] = 'previous ' + prev_button_props['class_name']
        if prev_button_props.get('style') is None:
            prev_button_props['style'] = {'float': 'left'}
        

        children = [
            html.Div(
                children=[
                    html.Div(id=self.ids.sleepy_div(yada_id),
                                   style={'height': '100%', 'width': '100%', 'position': 'absolute'},
                             className='sleepy_yada'),
                html.Img(
                    src=yada_src, className="sleeping"
                )],
                id=self.ids.dummy_div(yada_id),
                className=("yada sleeping" + yada_class).strip(),
            ),
            dcc.Store(id=self.ids.scripts(yada_id), data=scripts),
            dcc.Store(
                id=self.ids.sleep_message_greeting(yada_id),
                data=sleep_message_props["greeting"],
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader(
                        sleep_message_props["name"]
                        if sleep_message_props["name"]
                        else ""
                    ),
                    dbc.PopoverBody([
                            dcc.Markdown(
                                sleep_message_props["greeting"], id=self.ids.convo(yada_id), className="yada-convo"
                            ),
                            dbc.Button(**prev_button_props),
                            dbc.Button(**next_button_props),
                        ],
                        className="btn-info yada-info",
                    ),
                ],
                style={'zIndex':9999},
                target=self.ids.dummy_div(yada_id),
                trigger="hover",
                id=self.ids.sleep_message(yada_id),
            ),
            dbc.Popover(
                dbc.PopoverBody(
                    [
                        html.Div(children=[
                        html.Div(active_message),
                        dcc.Dropdown(id=self.ids.script_choices(yada_id), style={"minWidth": 350}),
                        dbc.Button(
                            **play_script_props, id=self.ids.play_script(yada_id)
                        ),
                        ], className='data_message'
                        ),
                        html.Div('Sorry, there are no scripts loaded', className='no_message')
                    ],
                    className='data' if scripts != {} else 'no_data',
                    id=self.ids.active_body(yada_id)
                ),
                style={"minWidth": 100},
                target=self.ids.sleepy_div(yada_id),
                delay={'show': 5},
                trigger="legacy",
                id=self.ids.active_message(yada_id),
            ),
        ]

        super(Yada, self).__init__(children)

    clientside_callback(
        """
        async function (n, s, o) {
            if (s) {return false}
            trig = JSON.parse(window.dash_clientside.callback_context.triggered[0].prop_id.split('.')[0])
            if (trig.subcomponent === 'active_message') {return window.dash_clientside.no_update}
            if (document.querySelector('.yada > img').classList.contains('sleeping')) {
                return !o
            }
            return window.dash_clientside.no_update
        }
        """,
        Output(ids.sleep_message(MATCH), "is_open"),
        Input(ids.dummy_div(MATCH), "n_clicks"),
        Input(ids.active_message(MATCH), "is_open"),
        State(ids.script_choices(MATCH), "is_open"),
        prevent_initial_call=True,
    )

    clientside_callback(
        """function (i, g) {
            if (!document.querySelector(".yada > img").classList.contains("sleeping")) {
                document.querySelector(".yada-info .next").style.display = 'initial'
                if (document.querySelector(".yada").getAttribute("convo")) {
                    if (window.dash_yada.y == 0) {
                        document.querySelector(".yada-info .previous").style.display = 'none'
                    } else {
                        document.querySelector(".yada-info .previous").style.display = 'initial'
                    }
                    document.querySelector(".yada-info .previous").addEventListener('click', 
                    function() {window.dash_yada.y = window.dash_yada.y-2, window.dash_yada.previous = true, window.dash_yada.paused = false})
                    document.querySelector(".yada-info .next").addEventListener('click', 
                    function() {window.dash_yada.yada.dispatchEvent(new Event('click'))})
                    return [document.querySelector(".yada").getAttribute("convo"), {hide: 1000}]
                }
                return ['', {hide: 50}]
            }
            try {
                document.querySelector(".yada-info .previous").style.display = 'none'
                document.querySelector(".yada-info .next").style.display = 'none'
            } catch {}
            return [g, {hide: 50}]
            
        }""",
        Output(ids.convo(MATCH), "children"),
        Output(ids.sleep_message(MATCH), "delay"),
        Input(ids.sleep_message(MATCH), "is_open"),
        State(ids.sleep_message_greeting(MATCH), "data"),
        prevent_initial_call=True,
    )

    clientside_callback(
        """
        function(o, d) {
            if (!document.querySelector('.yada > img').classList.contains('sleeping')) {
                return ['hidden', window.dash_clientside.no_update,  window.dash_clientside.no_update]
            }
            if (!d) {
                return ['', [], null]
            }
            return ['', Object.keys(d), Object.keys(d)[0]]
        }
        """,
        Output(ids.active_message(MATCH), "className"),
        Output(ids.script_choices(MATCH), "options"),
        Output(ids.script_choices(MATCH), "value"),
        Input(ids.active_message(MATCH), "is_open"),
        State(ids.scripts(MATCH), "data"),
        prevent_initial_call=True,
    )

    clientside_callback(
        """
            function (s, d) {
                if (s) {
                    if (Object.keys(d).length > 0) {
                        return 'data'
                    } else {
                        return 'no_data'
                    }
                }
                return window.dash_clientside.no_update
            }
        """,
        Output(ids.active_body(MATCH), "className"),
        Input(ids.active_message(MATCH), "is_open"),
        State(ids.scripts(MATCH), "data"),
        prevent_initial_call=True
    )

    clientside_callback(
        """
        function(c, v, d) {
            if (c) {
                if (v != '') {
                    play_script(d[v])
                    return [false, '']
                }
            }
            return [true, '']
        }
        """,
        Output(ids.active_message(MATCH), "is_open"),
        Output(ids.convo(MATCH), "children", allow_duplicate=True),
        Input(ids.play_script(MATCH), "n_clicks"),
        State(ids.script_choices(MATCH), "value"),
        State(ids.scripts(MATCH), "data"),
        prevent_initial_call=True,
    )
