from dash import html
from typing import Dict

def options(initial_theme:str, available_themes:Dict[str, str]) -> html.Div:
    options_div = html.Div(
        id="options",
        className="options-closed",
        children=[
            html.Div(id="options-header", 
                    className="options-header", 
                    children=[
                        html.Div(id="button-close-options", 
                                className="button-generic",
                                children=["CLOSE"],
                                n_clicks=0),
                        html.Div(className="flex_1"),
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
    return options_div