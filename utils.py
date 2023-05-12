from dash_yada import Yada

yada_test = Yada(
    yada_id="test",
    hover_message_props={
        "greeting": """
         _rawr!_  \r
          check out:  \r
          * 1  \r
          * 2  \r
          [markdown](#)
          """
    },
    script_message={"message": "testing"},
    play_script_props={"color": "warning", "children": "play"},
    scripts={
        "explore": [
            {
                "target": "#testing_type",
                "convo": "I can interact with input boxes",
                "action": "type",
                "action_args": "test",
            },
            {"target": "#test_click", "convo": "and click buttons", "action": "click"},
            {
                "target": "#modal .btn-close",
                "convo": "I can go onto modals",
                "action": "click",
            },
            {"target": "#grid", "convo": "I can highlight entire elements"},
            {
                "target": "#grid .ag-header-cell .ag-header-cell-label",
                "convo": "I can sort grids",
                "action": "click",
            },
            {
                "target": "#grid .ag-header-cell:nth-child(3) .ag-header-cell-label",
                "convo": "I can multi-sort grids",
                "action": "click",
                "action_args": {"shiftKey": True},
            },
            {
                "target": '.ag-row[row-index="2"] .ag-cell[aria-colindex="3"]',
                "action": "dblclick",
                "convo": "I can edit a grid",
            },
            {
                "target": '.ag-row[row-index="2"] .ag-cell[aria-colindex="3"] input',
                "action": "type",
                "convo": "I can edit a grid",
                "action_args": "testing",
            },
            {
                "target": '.ag-row[row-index="1"] .ag-cell[aria-colindex="3"]',
                "action": "click",
                "convo": "See?",
            },
            {
                "target": '.ag-row[row-index="1"] .ag-cell[aria-colindex="3"]',
                "convo": "I can even ctrl-z",
                "action": "sendKeys",
                "action_args": {
                    "ctrlKey": True,
                    "key": "z",
                    "code": "KeyZ",
                    "keyCode": 90,
                },
            },
            {
                "target": "#grid .ag-header-row-column-filter .ag-header-cell:nth-child(2)"
                " .ag-input-wrapper .ag-input-field-input",
                "convo": "I filter as well",
                "action": "type",
                "action_args": "BMW",
            },
            {
                "target": "#grid .ag-header-cell:nth-child(2)",
                "convo": "See!  \rI just applied a filter to this column",
            },
            {"target": "#testing", "convo": "I can even scroll"},
        ]
    },
    next_button_props={
        "size": "sm",
        "class_name": "fa-solid fa-arrow-right mb-2",
        "children": "",
    },
    prev_button_props={
        "size": "sm",
        "class_name": "fa-solid fa-arrow-left mb-2",
        "children": "",
    },
)
