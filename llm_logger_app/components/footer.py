from dash import html

def footer() -> html.Div:
    footer = html.Div(
        id="app-footer",
        className="footer",
        children=[
            html.Div(className="flex_1"),
            html.Div("E", className="button-generic"),
            html.Div(className="wedge_XS"),
            html.Div("F", className="button-generic"),
        ]
    )
    
    return footer