
<img src="dash_yada/tech-support.png" align="right" height="150px" />

# dash-yada  


__`dash-yada` lets you easily create interactive tutorials for your Dash app.__


### Installation

---

```bash
$ pip install dash-yada
```

### Live Demo

---

Check out the [Live Demo](https://dashyada.pythonanywhere.com/) to see dash-yada in action!

![yada_live_demo](https://github.com/BSd3v/dash-yada/assets/72614349/41039446-a460-425c-acd6-68a34749368f)

See the [code](https://github.com/BSd3v/dash-yada/tree/dev/docs/demo) for this demo in the docs folder.


### Quickstart  

---

Add yada to the app layout.  By default, the yada icon is a helpdesk, located in the top right corner of the site.  It displays a helpful welcome message on hover.
Everything is customizable, we'll show how later.

![yada_quickstart](https://github.com/BSd3v/dash-yada/assets/72614349/effe2931-b274-4e75-8ffe-03724b05d55c)

```python
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_yada import Yada

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        Yada(yada_id="yada"),
        html.H4("My Dashboard", className="p-3 bg-primary text-white text center"),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
```


### Adding scripts  

---

You can add one or more scripts for the user to select the tour.

Yada navigates by CSS selector, so it can go to any element on a page.  Learn more about selectors at [Mozilla web-docs](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector)
For example you could use a component's id like this:  `"#component_id"`.  You can use a class selector like this: `".close-btn"`

```
    - scripts (dict of list of dicts; optional):
        Dictionary of keys to scripts:
            - each key will have an array of a directory:
            {target (string; required), convo (string; required), action (string; optional),
            action_args (string; optional)}
```

Here is a simple example of one script that navigates to the header and gives an introduction.
You can find more script examples in the demo app.  The Yada component and the scripts are defined in a [yada_scripts.py file](https://github.com/BSd3v/dash-yada/blob/dev/docs/demo/yada_scripts.py), then imported in the app.

![yada_quickstart_script](https://github.com/BSd3v/dash-yada/assets/72614349/6971c5c7-cddb-4418-8853-64951384b7af)



```python
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_yada import Yada

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

yada = Yada(
    yada_id="yada",
    scripts={
        "Intro": [
            {
                "target": "#title",
                "convo": "Welcome to My Dashboard tour!",
            },
        ]
    },
)

app.layout = dbc.Container(
    [
        yada,
        html.H4(
            "My Dashboard",
            className="p-3 bg-primary text-white text center",
            id="title",
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
```


### Customizing the Yada Icon

You can change the icon by supplying another image to the `yada_src` prop
Change the welcome message and the name you see on hover when the script is not running with the `hover_message_props`
Set the position and size with CSS.  

For this example, place the followin in the .css file in the /assets folder

```css
.yada .sleeping {
    left: 75px;
    top: auto;
    bottom: 5px;
    height: 60px;
}
```

![yada_custom_icon](https://github.com/BSd3v/dash-yada/assets/72614349/14793b1e-9db4-4fd5-9fa3-bddaed0fa006)


```python

yada_icon = "https://user-images.githubusercontent.com/72614349/236646464-1471e596-b234-490d-bf84-e2ef7a63b233.png"
hover_message_props = {
    "name": "Hedwig",
    "greeting": "Let's explore! Just pick a tour and we'll get started"
}

yada = Yada(yada_id="my_yada", yada_src=yada_icon, hover_message_props=hover_message_props)

```



### Reference

---

dash-yada is an All-In-One component.  Learn more about AIO components in the [Dash documentation](https://dash.plotly.com/all-in-one-components).

```
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
```
