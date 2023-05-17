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

    - hover_message_props (dict; optional):
        Props to display for the message when yada is not clicked and not playing a script.
        If not defined, the default name is "yada".  Set name to "" to not display a header.  Set message to "" to not display a greeting
        If greeting or name is a component, it must be wrapped in [ ], for example {"greeting": [html.Div("Hi")]
        {name (string; optional), greeting (string; optional)}

    - script_message (dict; optional):
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
        steps_canvas = lambda yada_id: {
            "component": "yada",
            "subcomponent": "steps_canvas",
            "yada_id": yada_id,
        }
        canvas_button_open = lambda yada_id: {
            "component": "yada",
            "subcomponent": "canvas_button_open",
            "yada_id": yada_id,
        }

    ids = ids

    def __init__(
        self,
        hover_message_props={},
        script_message={},
        play_script_props={},
        yada_src=None,
        scripts=None,
        yada_id=None,
        yada_class="",
        prev_button_props={},
        next_button_props={},
        mobile_end_button_props={},
        offcanvas_style={},
    ):
        if yada_id is None:
            yada_id = str(uuid.uuid4())
        if yada_src is None:
            yada_src = "/_dash-component-suites/dash_yada/tech-support.png"

        default_greet = """
        Hello! I am Your Automated Dashboard Assistant.  
        But you can call me, Y.A.D.A!
        """

        hover_message_props = hover_message_props.copy()
        play_script_props = play_script_props.copy()
        prev_button_props = prev_button_props.copy()
        next_button_props = next_button_props.copy()
        mobile_end_button_props = mobile_end_button_props.copy()
        if scripts is None:
            scripts = addScripts()
        if hover_message_props:
            if hover_message_props.get("name") is None:
                hover_message_props["name"] = "yada"
            if hover_message_props.get("greeting") is None:
                hover_message_props["greeting"] = default_greet
            if hover_message_props.get("style") is None:
                hover_message_props["style"] = {}
        else:
            hover_message_props["name"] = "yada"
            hover_message_props["greeting"] = default_greet
            hover_message_props["style"] = {}
        if play_script_props:
            if play_script_props.get("children") is None:
                play_script_props["children"] = "play selected"
        else:
            play_script_props["children"] = "play selected"
        if script_message:
            if script_message.get("message") is None:
                script_message["message"] = "What would you like to do?"
            if script_message.get("style") is None:
                script_message["style"] = {}
        else:
            script_message["message"] = "What would you like to do?"
            script_message["style"] = {}

        if next_button_props.get("children") is None:
            next_button_props["children"] = "next"
        if next_button_props.get("class_name") is None:
            next_button_props["class_name"] = "next"
        else:
            next_button_props["class_name"] = "next " + next_button_props["class_name"]
        if next_button_props.get("style") is None:
            next_button_props["style"] = {"right": "0px"}

        if prev_button_props.get("children") is None:
            prev_button_props["children"] = "previous"
        if prev_button_props.get("class_name") is None:
            prev_button_props["class_name"] = "previous"
        else:
            prev_button_props["class_name"] = (
                "previous " + prev_button_props["class_name"]
            )
        if prev_button_props.get("style") is None:
            prev_button_props["style"] = {"left": "0px"}

        if mobile_end_button_props.get("style"):
            mobile_end_button_props["style"] = {
                **mobile_end_button_props["style"],
                "visibility": "hidden",
            }
        else:
            mobile_end_button_props["style"] = {"visibility": "hidden"}
        if mobile_end_button_props.get("size") is None:
            mobile_end_button_props["size"] = "sm"
        if mobile_end_button_props.get("class_name") is None:
            mobile_end_button_props["class_name"] = "exit"
        else:
            mobile_end_button_props["class_name"] = (
                mobile_end_button_props["class_name"] + " exit"
            )
        if mobile_end_button_props.get("children") is None:
            mobile_end_button_props["children"] = "end"

        children = [
            html.Div(
                children=[
                    html.Div(
                        id=self.ids.sleepy_div(yada_id),
                        style={
                            "height": "100%",
                            "width": "100%",
                            "position": "absolute",
                        },
                        className="sleepy_yada",
                    ),
                    html.Img(src=yada_src, className="sleeping"),
                ],
                id=self.ids.dummy_div(yada_id),
                className=("yada sleeping " + yada_class).strip(),
            ),
            html.Button(
                id=self.ids.canvas_button_open(yada_id),
                n_clicks=0,
                className="yada_canvas_button_open",
                style={"display": "none"},
            ),
            dcc.Store(id=self.ids.scripts(yada_id), data=scripts),
            dcc.Store(
                id=self.ids.sleep_message_greeting(yada_id),
                data=hover_message_props["greeting"],
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader(hover_message_props["name"]),
                    dbc.PopoverBody(
                        [
                            dcc.Markdown(
                                hover_message_props["greeting"],
                            ),
                        ],
                        style=hover_message_props["style"],
                    ),
                ],
                style={"zIndex": 9999},
                target=self.ids.sleepy_div(yada_id),
                trigger="hover",
                id=self.ids.sleep_message(yada_id),
            ),
            dbc.Popover(
                dbc.PopoverBody(
                    [
                        html.Div(
                            children=[
                                html.Div(script_message["message"]),
                                dcc.Dropdown(
                                    id=self.ids.script_choices(yada_id),
                                    style={"minWidth": 250},
                                ),
                                dbc.Button(
                                    **play_script_props,
                                    id=self.ids.play_script(yada_id)
                                ),
                            ],
                            className="data_message",
                        ),
                        html.Div(
                            "Sorry, there are no scripts loaded", className="no_message"
                        ),
                    ],
                    className="data" if scripts != {} else "no_data",
                    id=self.ids.active_body(yada_id),
                    style=script_message["style"],
                ),
                style={"minWidth": 100},
                target=self.ids.sleepy_div(yada_id),
                delay={"show": 5},
                trigger="legacy",
                id=self.ids.active_message(yada_id),
            ),
            dbc.Offcanvas(
                children=[
                    dcc.Markdown(
                        id=self.ids.convo(yada_id),
                        className="yada-convo",
                        link_target="_blank"
                    ),
                ],
                className="yada-info",
                id=self.ids.steps_canvas(yada_id),
                backdrop=False,
                placement="bottom",
                scrollable=True,
                title=dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(**prev_button_props),
                            width=2,
                            style={"justifyContent": "center", "display": "flex"},
                        ),
                        dbc.Col(width=3),
                        dbc.Col(
                            dbc.Button(**mobile_end_button_props),
                            width=2,
                            style={"justifyContent": "center", "display": "flex"},
                        ),
                        dbc.Col(width=3),
                        dbc.Col(
                            dbc.Button(**next_button_props),
                            width=2,
                            style={"justifyContent": "center", "display": "flex"},
                        ),
                    ],
                    style={"maxWidth": "95%"},
                ),
                style=offcanvas_style,
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
        prevent_initial_call=True,
    )

    clientside_callback(
        """
        function(c, v, d) {
            if (c) {
                if (v != '') {
                    window.dash_yada.close_statement = d[v][d[v].length-1].convo
                    play_script(d[v])
                    return false
                }
            }
            return true
        }
        """,
        Output(ids.active_message(MATCH), "is_open"),
        Input(ids.play_script(MATCH), "n_clicks"),
        State(ids.script_choices(MATCH), "value"),
        State(ids.scripts(MATCH), "data"),
        prevent_initial_call=True,
    )
    clientside_callback(
        """
            function (p) {
                return true
            }
        """,
        Output(ids.steps_canvas(MATCH), "is_open"),
        Input(ids.play_script(MATCH), "n_clicks"),
        prevent_initial_call=True,
    )

    clientside_callback(
        """function (s) {
                if (!document.querySelector(".yada > img").classList.contains("sleeping")) {
                    if (document.querySelector(".yada").getAttribute("convo")) {
                        return document.querySelector(".yada").getAttribute("convo")
                    }
                }
                return window.dash_clientside.no_update
        }""",
        Output(ids.convo(MATCH), "children"),
        Input(ids.steps_canvas(MATCH), "is_open"),
    )

    clientside_callback(
        """function (o) {
        if (o) {
            previous = () =>
            { window.dash_yada.y = window.dash_yada.y - 2;
             window.dash_yada.previous = true;
              window.dash_yada.paused = false}
              
            exit = () =>
            {document.dispatchEvent(new KeyboardEvent('keydown', {bubbles: true, key: "Escape", code: "Escape", which: 27}))}
            
            next = () => {window.dash_yada.yada.dispatchEvent(new Event('click'))}
            
            if (/Android|iPhone/i.test(navigator.userAgent)) {
                document.querySelector(".yada-info .exit").style.visibility = ""
            }
        
            if (!window.dash_yada.y) {
                document.querySelector(".yada-info .next").style.display = "initial"
            } else if (window.dash_yada.y < window.dash_yada.script_length) {
                document.querySelector(".yada-info .next").style.display = "initial"
            }
            if (!document.querySelector(".yada-info .previous").getAttribute('listener')) {
                document.querySelector(".yada-info .previous").addEventListener('click', previous)
                document.querySelector(".yada-info .previous").setAttribute('listener', true);
                document.querySelector(".yada-info .next").addEventListener('click', next)
                document.querySelector(".yada-info .exit").addEventListener('click', exit)
            }

        }
        return window.dash_clientside.no_update
    }""",
        Output(ids.steps_canvas(MATCH), "id"),
        Input(ids.steps_canvas(MATCH), "is_open"),
    )

    clientside_callback(
        """function (n) {
                if (!document.querySelector(".yada > img").classList.contains("sleeping")) {
                    if (document.querySelector(".yada").getAttribute("convo")) {
                        return [document.querySelector(".yada").getAttribute("convo"), true, window.dash_yada.placement]
                    }
                }
                return [window.dash_clientside.no_update, window.dash_clientside.no_update, window.dash_yada.placement]
        }""",
        Output(ids.convo(MATCH), "children", allow_duplicate=True),
        Output(ids.steps_canvas(MATCH), "is_open", allow_duplicate=True),
        Output(ids.steps_canvas(MATCH), "placement"),
        Input(ids.canvas_button_open(MATCH), "n_clicks"),
        prevent_initial_call=True,
    )
