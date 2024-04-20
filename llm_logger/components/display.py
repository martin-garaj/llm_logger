
from dash import html, dcc

def display() -> html.Div:

    display_div = html.Div(className="display-content", 
                    children=[
                        html.Div(id="display", 
                                className="display", 
                                children=[dcc.Markdown("fdsdfsf<br> szdfasdf")]),
                ])
    
    return display_div