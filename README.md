
<img src="dash_yada/tech-support.png" align="right" height="150px" />

# dash-yada  


__`dash-yada` lets you easily create interactive tutorials for your Dash app.__


### Installation

---

```bash
$ pip install dash-yada
```

<br>
<br>

### Live Demo

---

Check out the [Live Demo](https://dashyada.pythonanywhere.com/) to see dash-yada in action!

See the [code](https://github.com/BSd3v/dash-yada/tree/dev/docs/demo) for this demo in the /docs folder.

![yada_demo_dev_intro](https://github.com/BSd3v/dash-yada/assets/72614349/bdb46af3-26df-49b7-be8b-a035eebb169c)


<br>
<br>


### Quickstart  

---

To get started, simply add the `Yada()` component to the app's layout. 
You will see the Yada icon, a helpdesk, in the top right corner.  On hover, it displays a default welcome message.

![yada_quickstart](https://github.com/BSd3v/dash-yada/assets/72614349/effe2931-b274-4e75-8ffe-03724b05d55c)

```python
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_yada import YadaAIO

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        YadaAIO(yada_id="yada"),
        html.H4("My Dashboard", className="p-3 bg-primary text-white text center"),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)

```

<br>
<br>

### Customizing the Yada Icon

-----

Use the following props to change the icon and the hover message:

- `yada_src` (string; optional): Location src of the image that you want to display for yada.

- `hover_message_props` (dict; optional):
        Props to display for the message when yada is not clicked and not playing a script.
        If not defined, the default name is "yada".  Set name to "" to not display a header.  Set message to "" to not display a greeting
        {name (string; optional), greeting (string; optional)}

- Set the position and size with CSS:

For this example, place the following in the .css file in the /assets folder

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

yada = YadaAIO(yada_id="my_yada", yada_src=yada_icon, hover_message_props=hover_message_props)


```

 
<br>
<br>



### Adding scripts  

---

You can add one or more scripts for the user to select the tour.

Yada navigates by CSS selector, so it can go to any element on a page.  Learn more about selectors at [Mozilla web-docs](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector)
For example you could use a component's id like this:  `"#component_id"`.  You can use a class selector like this: `".close-btn"`


- `scripts` (dict of list of dicts; optional):  Dictionary of keys to scripts:
    - each key will have an array of:
    {target (string; required), convo (string; required), action (string; optional), action_args (string; optional)}


Here is a simple example of one script with one step. You can find more script examples in the demo app: [yada_scripts.py file](https://github.com/BSd3v/dash-yada/blob/dev/docs/demo/yada_scripts.py)

![yada_quickstart_script](https://github.com/BSd3v/dash-yada/assets/72614349/6971c5c7-cddb-4418-8853-64951384b7af)



```python
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_yada import YadaAIO

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

yada = YadaAIO(
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

<br>
<br>


### Reference

---

dash-yada.YadaAIO is an All-In-One component.  Learn more about AIO components in the [Dash documentation](https://dash.plotly.com/all-in-one-components).

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
