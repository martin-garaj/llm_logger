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
            html.Div(className="flex_1"),
            html.Div(id="button-open-upload", 
                     className="button-generic",
                     children=["UPLOAD"],
                    n_clicks=0),
        ]
    )
    
    return header_div
