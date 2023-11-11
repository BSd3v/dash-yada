from dash import Dash, dcc
import dash_bootstrap_components as dbc
from dash_yada import YadaAIO

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

yada_img = "https://user-images.githubusercontent.com/72614349/236646464-1471e596-b234-490d-bf84-e2ef7a63b233.png"

hover_message_dict = {
    "name": "Hedwig",
    "greeting": "Let's explore! Just pick a tour and we'll get started",
    "style": {"backgroundColor": "lightgreen"}
}

yada = YadaAIO(
    yada_id="my-yada", yada_src=yada_img, hover_message_dict=hover_message_dict
)

content = dcc.Markdown("""

This example shows how to customize and style the yada image and the hover message.  

### Custom yada image
Use the `yada_src` prop to use your own image instead of the default. This example uses an external link. Or you can
 specify a path to a file, for example:
 
 ```python
 YadaAIO(yada_src="assets/my-image.png") 
 ```

### Styling the yada image
Use CSS to position and style the Yada image.

Use the `.yada.sleeping` classes to style the icon before the tour starts.

The default is:

```css

.yada.sleeping {
    right: 30px;
    top: 5px;
    height: 50px;
    width: 35px;
}
```

### Setting the hover message

Use the `hover_message_dict` prop to customize the hover message.  The dict has three keys, the `"name"`, `"greeting"` and `"style"`.

This example uses:

```
hover_message_dict = {
    "name": "Hedwig",
    "greeting": "Let's explore! Just pick a tour and we'll get started",
    "style": {"backgroundColor": "lightgreen"}
}
```

If you would like to hover message to be open when the app starts, you can use this callback:

```
clientside_callback(
    "function () {return true}",
    Output(yada.ids.hover_message("my-yada"), "is_open"),
    Input(yada.ids._dummy_div("my-yada"), "id"),
)
```

""", className="mt-5")

app.layout = dbc.Container([yada, content])


if __name__ == "__main__":
    app.run_server(debug=True)
