from dash_yada import Yada

yada = Yada(
    yada_id="demo",
    next_button_props={
        "size": "sm",
    },
    prev_button_props={
        "size": "sm",
        "children": "Prev",
    },
    scripts={
        "explore": [

            {
                "target": "#title",
                "convo": "I'll show you how to create a fun interactive demo so people can get the most out of your site. \r\r I can go to any element on the page.  I navigate by component id or className."
            },
            {
                "target": "#title",
                "convo": "We are now at the `#title`.  Here you can describe the overiview and purpose of the site.  \r\r Next, I'll show how to filter the AG Grid component."
            },
            {
                "target": "#quick-filter-input",
                "convo": "I can interact with input boxes.  This input is a 'quick filter' for the grid.  \r\r Next I'll type 'Rep Africa'.",
                "action": "type",
                "action_args": "Rep Africa",
            },
            {
                "target": "#quick-filter-input",
                "convo": "See!  It now only displays rows with both 'Rep' AND 'Africa' in them. ",
            },
            {
                "target": "#pop",
                "convo": "You can also explain other interactivity as well.  For example, in this app the figures are updated too.",
            },
            {
                "target": "#title",
                "convo": "Now try it yourself!  Go ahead and enter something into the input field.  I'll wait here."

            },
            {
                "target": "#quick-filter-input",
                "convo": "Next, I'll clear the filter so you can see all the data again.",
                "action": "type",
                "action_args": "",
            },
        ]
    },
)
