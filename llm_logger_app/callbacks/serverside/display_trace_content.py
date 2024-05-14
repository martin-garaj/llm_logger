from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html, no_update


def register_display_trace_content(app):
    @app.callback(
        Output('display', 'children'),
        Input('fig-graph', 'clickData'),
    )
    def display_trace_content(clickData):


        if clickData is None:
            lines = ["Select node in graph."]
        else:
            try:
                lines = str(clickData['points'][0]['customdata'][0]\
                    ["data"]["content"]).split('\n')
                
            except KeyError:
                return no_update
                
        divs = list()

        divs.append(
            html.Div(
                children=[
                    html.Div(className="display-line-num"),
                    html.Div(className="display-line-text"),
                ],
                className="display-line display-start",
            )
        )

        for line_idx, line in enumerate(lines):
            divs.append(
                html.Div(
                    children=[
                        html.Div(children=f"{line_idx+1}", className="display-line-num"),
                        html.Div(children=f"{line}", className="display-line-text"),
                    ],
                    className="display-line"
                )
            )

        divs.append(
            html.Div(
                children=[
                    html.Div(className="display-line-num"),
                    html.Div(className="display-line-text"),
                ],
                className="display-line display-end",
            )
        )

        return divs
