from dash_yada import YadaAIO
from dash import callback, Input, Output


off_canvas_style = {
    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
    "margin": "8px auto",
    "padding": "0px 24px 5px",
    "backgroundColor": "var(--bs-gray-500)",
    "color": "white",
    "borderRadius": 12,
    "maxWidth": 800,
}


housekeeping_script = [
    {
        "target": ".title",
        "convo": """
                First, a few housekeeping notes:            
                - You can close this dialogue box to see the whole screen, then click on me to continue
                - Press the escape key any time to exit the tour                   
                """,
    },
]

dev_intro_script = (
    [
        {
            "target": "#title",
            "convo": "##### I'll show you how to create a fun interactive demo so people can get the most out of your site.",
        }
    ]
    + housekeeping_script
    + [
        {
            "target": "#title",
            "convo": """
                I navigate using [selectors](https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector) so I can go to any element on the page.        
                We are now at the title.  Here you can describe the overview and purpose of your site.  
                Next, I'll show how to filter the AG Grid component.
                """,
        },
    ]
)

filter_script = [
    {
        "target": "#quick-filter-input",
        "convo": "This input is a 'quick filter' for the grid.  \r\r Click Next, and I'll type 'Rep Africa' for you.",
        "action": "type",
        "action_args": "Rep Africa",
    },
    {
        "target": "#quick-filter-input",
        "convo": "Now the grid only displays rows with both 'Rep' AND 'Africa'. ",
    },
    {
        "target": "#Population",
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
    {
        "target": "#grid .ag-header-cell:nth-child(4) .ag-header-cell-label",
        "convo": """
        In the column headers  you'll find  more filter options.   
        
        On a desktop, hover over the header and you'll see a menu icon to click.  On a touchscreen, press and hold
         the header and the popup filter dialog box will appear.  
         
        Give it a try!
        """,
    },
]

dev_sort_script = [
    {
        "target": "#grid .ag-header-cell:nth-child(2) .ag-header-cell-label",
        "convo": "You can sort the grid by clicking on the header",
        "action": "click",
    },
    {
        "target": "#grid .ag-header-cell:nth-child(3) .ag-header-cell-label",
        "convo": "You can multi-sort grids by holding down the shift key while clicking the header.",
        "action": "click",
        "action_args": {"shiftKey": True},
    },
    {
        "target": "#grid .ag-header-cell:nth-child(4) .ag-header-cell-label",
        "convo": "Note that the grid is now sorted by continent, then by population.  The figures updated too!",
    },
]

dev_edit_script = [
    {
        "target": '.ag-row[row-index="2"] .ag-cell[aria-colindex="3"]',
        "action": "dblclick",
        "convo": "You can edit the grid by double clicking on the cell",
    },
    {
        "target": '.ag-row[row-index="2"] .ag-cell[aria-colindex="3"] input',
        "action": "type",
        "convo": "Let's update the population",
        "action_args": "900000000",
    },
    {
        "target": '.ag-row[row-index="0"] .ag-cell[aria-colindex="3"]',
        "action": "click",
        "convo": "",
    },
    {
        "target": '.ag-row[row-index="2"] .ag-cell[aria-colindex="3"]',
        "convo": "To undo a change type ctrl-z.  If you are on a desktop - give it a try!",
        "action": "click",
    },
]

dev_conclusion_script = [
    {
        "target": "#title",
        "convo": """
        Be sure to check out my [Github](https://github.com/BSd3v/dash-yada) for more information on how to customize me, including my icon, scripts and style.  
        
        I hope you enjoyed the tour.  Happy exploring!!
        """,
    }
]

conclusion_script = [
    {"target": "#title", "convo": "I hope you enjoyed the tour.  Happy exploring!!"}
]


user_intro_script = (
    [
        {
            "target": "#title",
            "convo": """
        This site has information about the population, life expectancy and GDP per capita in different countries
         of the world.  The data is from 2007.  
         
         On this tour,  I'll give you a overview to help you get started exploring the data.
         """,
        },
    ]
    + housekeeping_script
    + [
        {
            "target": "#grid .ag-header-cell:nth-child(2) .ag-header-cell-label",
            "convo": """
        Here  the data is in a table with 5 columns: Country, Continent, Population, Life Expectancy and GDP Per Capita in US dollars.  
        
        Below the table, you'll find three bar charts. The X axis is the Country column. The Y axis is one of Population, Life Expectancy or GDP per capita.   
        """,
        },
        {
            "target": "#Population",
            "convo": """
        For example, this chart show population by country.  Note that when you interact with the grid, the figures
         will update too.  Next, I'll show you how.
         """,
        },
    ]
)

user_sort_script = [
    {
        "target": "#grid .ag-header-cell:nth-child(3) .ag-header-cell-label",
        "convo": """
        Sorting the columns is a quick way to see the min and max values.  Click next and I'll click on the header of
        the Population column. You'll see the table will then be sorted  ascending by Population. Note all three bar 
        charts below are updated when the table is sorted.
        """,
        "action": "click",
    },
    {
        "target": "#grid .ag-header-cell:nth-child(3) .ag-header-cell-label",
        "convo": """
        Click "next" again, and I'll click on the Population column header again, so it sorts descending
        """,
        "action": "click",
    },
    {
        "target": "#title",
        "convo": """
        Now try sorting the other columns as well.  I'll wait here.   
        
        When you're ready, click the 'next'  button. 
        """,
    },
]

yada = YadaAIO(
    yada_id="demo",
    next_button_props={
        "size": "sm",
    },
    prev_button_props={
        "size": "sm",
        "children": "prev",
    },
    steps_offcanvas_style=off_canvas_style,
    scripts={
        "Intro tour for developers": dev_intro_script
        + filter_script
        + dev_sort_script
        + dev_edit_script
        + dev_conclusion_script,
        "Intro tour for users": user_intro_script
        + user_sort_script
        + filter_script
        + conclusion_script,
        "Filter": filter_script + conclusion_script,
        "Sort": dev_sort_script + conclusion_script,
        "Edit": dev_edit_script + conclusion_script,
    },
)
