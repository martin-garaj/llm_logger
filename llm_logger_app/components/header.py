from dash import html

def header() -> html.Div:
    header_div = html.Div(
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
    
    return header_div
