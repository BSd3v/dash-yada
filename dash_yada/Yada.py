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


class YadaAIO(html.Div):
    """A html.Div All-in-One component.

    Keyword arguments:

    - yada_id (string; optional):
        The ID used to identify this component in Dash callbacks.

    - hover_message_dict (dict; optional {name, greeting, style}):
        Props to display for the message when yada is not clicked and not playing a script.
        If not defined, the default name is "yada".  Set name to "" to not display a header.  Set message to "" to not display a greeting
        {name (string; optional), greeting (string; optional), style (dict; optional}

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

    - end_button_props (dict; optional):
        Props to control the options for the end button. dbc.Button props.

    - steps_offcanvas_style (dict; optional):
        Style to control the offcanvas style while playing a script.

    """

    class ids:
        hover_message = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "hover_message",
            "yada_id": yada_id,
        }
        hover_message_greeting = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "hover_message_greeting",
            "yada_id": yada_id,
        }
        convo = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "convo",
            "yada_id": yada_id,
        }
        active_message = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "active_message",
            "yada_id": yada_id,
        }
        active_body = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "active_body",
            "yada_id": yada_id,
        }
        scripts = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "scripts",
            "yada_id": yada_id,
        }
        script_choices = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "script_choices",
            "yada_id": yada_id,
        }
        _dummy_div = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "_dummy_div",
            "yada_id": yada_id,
        }
        sleepy_div = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "sleepy_div",
            "yada_id": yada_id,
        }
        play_script = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "play_script",
            "yada_id": yada_id,
        }
        _steps_offcanvas = lambda yada_id: {  ## <- internal use with children/title/className, do not update children/title/className, or break scripts
            "component": "YadaAIO",
            "subcomponent": "_steps_offcanvas",
            "yada_id": yada_id,
        }
        canvas_button_open = lambda yada_id: {
            "component": "YadaAIO",
            "subcomponent": "canvas_button_open",
            "yada_id": yada_id,
        }

    ids = ids

    def __init__(
        self,
        hover_message_dict={},
        script_message={},
        play_script_props={},
        yada_sleep_src=None,
        yada_active_src=None,
        scripts=None,
        yada_id=None,
        yada_class="",
        prev_button_props={},
        next_button_props={},
        end_button_props={},
        steps_offcanvas_style={},
    ):
        if yada_id is None:
            yada_id = str(uuid.uuid4())
        if yada_sleep_src is None:
            yada_sleep_src = "/_dash-component-suites/dash_yada/yada.png"

        default_greet = """
        Hello!  \r         
        I'm Your Automated Dashboard Assistant.  
        But you can call me Y.A.D.A!  
        
        ##### Click on me to get started ↗️
        """

        default_steps_offcanvas_style = {"flexDirection": "column-reverse"}
        if steps_offcanvas_style:
            steps_offcanvas_style = {
                **default_steps_offcanvas_style,
                **steps_offcanvas_style,
            }
        else:
            steps_offcanvas_style = default_steps_offcanvas_style

        hover_message_dict = hover_message_dict.copy()
        play_script_props = play_script_props.copy()
        prev_button_props = prev_button_props.copy()
        next_button_props = next_button_props.copy()
        end_button_props = end_button_props.copy()
        if scripts is None:
            scripts = addScripts()
        if hover_message_dict:
            if hover_message_dict.get("name") is None:
                hover_message_dict["name"] = "yada"
            if hover_message_dict.get("greeting") is None:
                hover_message_dict["greeting"] = default_greet
            if hover_message_dict.get("style") is None:
                hover_message_dict["style"] = {}
        else:
            hover_message_dict["name"] = "yada"
            hover_message_dict["greeting"] = default_greet
            hover_message_dict["style"] = {}
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

        if end_button_props.get("size") is None:
            end_button_props["size"] = "sm"
        if end_button_props.get("class_name") is None:
            end_button_props["class_name"] = "exit"
        else:
            end_button_props["class_name"] = end_button_props["class_name"] + " exit"
        if end_button_props.get("children") is None:
            end_button_props["children"] = "end"

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
                    html.Img(src=yada_sleep_src, className="yada-img sleep sleeping"),
                    html.Img(
                        src=yada_active_src or yada_sleep_src,
                        className="yada-img active",
                    ),
                ],
                id=self.ids._dummy_div(yada_id),
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
                id=self.ids.hover_message_greeting(yada_id),
                data=hover_message_dict["greeting"],
            ),
            dbc.Popover(
                [
                    dbc.PopoverHeader(hover_message_dict["name"]),
                    dbc.PopoverBody(
                        [
                            dcc.Markdown(
                                hover_message_dict["greeting"],
                            ),
                        ],
                        style=hover_message_dict["style"],
                    ),
                ],
                style={"zIndex": 9999},
                target=self.ids.sleepy_div(yada_id),
                trigger="hover",
                class_name="yada-hover-message",
                id=self.ids.hover_message(yada_id),
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
                class_name="yada-active-message",
                id=self.ids.active_message(yada_id),
            ),
            dbc.Offcanvas(
                children=[
                    dcc.Markdown(
                        id=self.ids.convo(yada_id),
                        className="yada-convo",
                        link_target="_blank",
                    ),
                ],
                className="yada-info",
                id=self.ids._steps_offcanvas(
                    yada_id
                ),  ## <- internal use with children/title/className, do not update children/title/className, or break scripts
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
                            dbc.Button(**end_button_props),
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
                ),
                style=steps_offcanvas_style,
            ),
        ]

        super(YadaAIO, self).__init__(children)

    clientside_callback(
        """
        async function (n, s, o) {
            if (s) {
                document.querySelector('.yada').classList.add('activated')
                return false
            }
            document.querySelector('.yada').classList.remove('activated')
            trig = JSON.parse(window.dash_clientside.callback_context.triggered[0].prop_id.split('.')[0])
            if (trig.subcomponent === 'active_message') {return window.dash_clientside.no_update}
            if (document.querySelector('.yada > img').classList.contains('sleeping')) {
                return true
            }
            return window.dash_clientside.no_update
        }
        """,
        Output(ids.hover_message(MATCH), "is_open", allow_duplicate=True),
        Input(ids._dummy_div(MATCH), "n_clicks"),
        Input(ids.active_message(MATCH), "is_open"),
        State(ids.script_choices(MATCH), "is_open"),
        prevent_initial_call=True,
    )

    clientside_callback(
        """
        async function (s, o) {
            if (o) {
                return false
            }
            if (document.querySelector('.yada > img').classList.contains('sleeping')) {
                return s
            }
            return false
        }
        """,
        Output(ids.hover_message(MATCH), "is_open", allow_duplicate=True),
        Input(ids.hover_message(MATCH), "is_open"),
        State(ids.active_message(MATCH), "is_open"),
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
        Output(ids._steps_offcanvas(MATCH), "is_open"),
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
        Input(ids._steps_offcanvas(MATCH), "is_open"),
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
        
            if (!window.dash_yada.y) {
                document.querySelector(".yada-info .next").style.display = "initial"
            } else if (window.dash_yada.y < window.dash_yada.script_length-1) {
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
        Output(ids._steps_offcanvas(MATCH), "id"),
        Input(ids._steps_offcanvas(MATCH), "is_open"),
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
        Output(ids._steps_offcanvas(MATCH), "is_open", allow_duplicate=True),
        Output(ids._steps_offcanvas(MATCH), "placement"),
        Input(ids.canvas_button_open(MATCH), "n_clicks"),
        prevent_initial_call=True,
    )
