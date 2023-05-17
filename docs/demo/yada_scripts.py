from dash_yada import Yada


intro_script = [
    {
        "target": "#title",
        "convo": "##### I'll show you how to create a fun interactive demo so people can get the most out of your site.",
    },
    {
        "target": ".alert .btn-close",
        "convo": """
                First, a few housekeeping notes:            
                - You can close this dialogue box to see the whole screen, then click on me to continue
                - Press the escape key any time to exit the demo             
                When you're ready click the 'next' button.  I'll close the alert, then we'll begin.
                """,
        "action": "click",
    },
    {
        "target": "#title",
        "convo": """
                I navigate using [selectors](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector) so I can go to any element on the page.        
                We are now at the `#title`.  Here you can describe the overview and purpose of your site.  
                Next, I'll show how to filter the AG Grid component.
                """,
    },
]

filter_scirpt = [
    {
        "target": "#quick-filter-input",
        "convo": "I can interact with input boxes.  This input is a 'quick filter' for the grid.  \r\r Next I'll type 'Rep Africa'.",
        "action": "type",
        "action_args": "Rep Africa",
    },
    {
        "target": "#quick-filter-input",
        "convo": "See!  The grid now only displays rows with both 'Rep' AND 'Africa'. ",
    },
    {
        "target": "#pop",
        "convo": "Note that the figures are updated when the grid is filtered.",
    },
    {
        "target": "#title",
        "convo": "Now try it yourself!  Go ahead and enter something into the input field.  I'll wait here.",
    },
    {
        "target": "#quick-filter-input",
        "convo": "Next, I'll clear the filter so you can see all the data again.",
        "action": "type",
        "action_args": "",
    },
]

sort_script = [
    {
        "target": "#grid .ag-header-cell:nth-child(2) .ag-header-cell-label",
        "convo": "You can sort the grid by clicking on the header",
        "action": "click",
    },
    {
        "target": "#grid .ag-header-cell:nth-child(4) .ag-header-cell-label",
        "convo": "You can multi-sort grids by holding down the shift key while clicking the header.",
        "action": "click",
        "action_args": {"shiftKey": True},
    },
    {
        "target": "#grid .ag-header-cell:nth-child(4) .ag-header-cell-label",
        "convo": "Note that the grid is now sorted by continent, then by population.  The figures updated too!",
    },
]

edit_script = [
    {
        "target": '.ag-row[row-index="2"] .ag-cell[aria-colindex="4"]',
        "action": "dblclick",
        "convo": "You can edit the grid by double clicking on the cell",
    },
    {
        "target": '.ag-row[row-index="2"] .ag-cell[aria-colindex="4"] input',
        "action": "type",
        "convo": "Let's update the population",
        "action_args": "900000000",
    },
    {
        "target": '.ag-row[row-index="1"] .ag-cell[aria-colindex="3"]',
        "action": "click",
        "convo": "Note that selected rows are a different color in the figures",
    },
    {
        "target": "#gdpPercap",
        "convo": "",
    },
    {
        "target": '.ag-row[row-index="1"] .ag-cell[aria-colindex="3"]',
        "convo": "To undo a change type ctrl-z.  If you are on a desktop - give it a try!",
    },
]

conclusion_script = [{"target": "#title", "convo": "I hope you enjoyed the tour!"}]

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
        "Explore": intro_script
        + filter_scirpt
        + sort_script
        + edit_script
        + conclusion_script,
        "Filter": filter_scirpt,
        "Sort": sort_script,
        "Edit": edit_script,
    },
)
