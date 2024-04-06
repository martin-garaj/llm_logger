"""
export PYTHONPATH="${PYTHONPATH}:/home/gartin/Documents/AlphaPrompt/Fairy_tales/Projects/llm_logger/llm_logger"

lsof -i :8050
kill -9 <PID>
"""

from dash import Dash, html, dcc



################################################################################
##                               initialization                               ##
################################################################################

initial_theme = 'light'
available_themes = dict(
    light="LIGHT",
    dark="DARK"
    
)

################################################################################
##                               html structure                               ##
################################################################################
app = Dash(
    __name__,
)


header = html.Div(
    id="app-header",
    className="header",
    children=[
        html.Div(id="button-open-options", 
                 className="button-generic", 
                 children=["OPTIONS"],
                 n_clicks=0),
        html.Div(id="flex", 
                 className="flex_1"),
        html.Div("B", 
                 className="button-generic", 
                 n_clicks=0),
        html.Div(id="flex", 
                 className="flex_1"),
        html.Div("C", 
                 className="button-generic",
                 n_clicks=0),
    ]
)

options = html.Div(
    id="options",
    className="options",
    children=[
        html.Div(id="options-header", 
                 className="options-header", 
                 children=[
                    html.Div(id="button-close-options", 
                             className="button-generic",
                             children=["CLOSE"],
                             n_clicks=0),
                    html.Div(id="flex", className="flex_1"),
                ]),
        html.Div(id="options-content", 
                 className="options-content",
                 children=[
                     html.Div(id="button-theme", 
                              className="button-theme",
                              children=[available_themes[initial_theme]],
                              n_clicks=0),
                     ]),
        ],
)

footer = html.Div(
    id="app-footer",
    className="footer",
    children=[
        html.Div(id="flex", className="flex_1"),
        html.Div("E", className="button-generic"),
        html.Div(id="flex", className="wedge_XS"),
        html.Div("F", className="button-generic"),
    ]
)


chapters = list()
chapters.append(html.Div(f"{1}",  className="fig-chapter"))
chapters.append(html.Div(f"{2}",  className="fig-chapter"))
chapters.append(html.Div(f"{3}",  className="fig-chapter"))
chapters.append(html.Div(f"{4}",  className="fig-chapter-selected"))
chapters.extend([html.Div(f"{i}", className="fig-chapter") for i in range(5,35)])


main_left = html.Div(
    id="main-left",
    className="main-left",
    children=[
        html.Div(
            id="fig-content",
            className="fig-content",
            children=[ 
                html.Div(id="fig-blank",  className="fig-blank"),
                html.Div(id="fig-title",  className="fig-title"),
                html.Div(id="fig-index",  className="fig-index hide-scrollbar", children=chapters),
                html.Div(id="fig-plotly", className="fig-plotly"),
                      ],
            ),
        ],
)

main_right = html.Div(
    id="main-right",
    className="main-right",
    children=[
        html.Div(className="display-content", 
                 children=[
                    html.Div(id="display", 
                             className="display", 
                             children=[dcc.Markdown("fdsdfsf <br> szdfasdf")]),
            ]),
        ],
)

main = html.Div(
    id="main",
    className="main-content",
    children=[
        main_left,
        main_right,
    ],
)

app.layout = html.Div(
    id="app",
    className="app",
    children=[
        options,
        header,
        main,
        footer],
    **{"data-theme": initial_theme},

)





################################################################################
##                               html structure                               ##
################################################################################
from dash import html, Input, Output, State, callback_context

@app.callback(
    Output("options", "className"),
    [Input("button-open-options", "n_clicks"), Input("button-close-options", "n_clicks")],
)
def toggle_menu(open_clicks, close_clicks):
    ctx = callback_context

    # If no buttons were clicked yet, keep the menu hidden
    if not ctx.triggered:
        return "options"

    # Determine which button was clicked
    last_triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If the 'open-menu-button' was clicked, show the menu, else hide it
    if last_triggered_id == 'button-open-options':
        return "options-open"
    else:  # This would be 'close-menu-button' or any other close trigger
        return "options"


@app.callback(
    [Output('app', 'data-theme'),
     Output('button-theme', 'children')],
    [Input('button-theme', 'n_clicks'),
     State('app', 'data-theme')],
    prevent_initial_call=True
)
def switch_theme(n_clicks, data_theme):
    print(data_theme)
    if n_clicks % 2:
        return 'dark', ["DARK"] 
    else:
        return 'light', ["LIGHT"]



if __name__ == '__main__':
    from dash import html
    from dash import Dash

    app.run_server(debug=False)
