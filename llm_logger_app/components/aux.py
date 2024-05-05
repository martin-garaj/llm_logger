from dash import html, dcc

def aux() -> html.Div:

    aux = html.Div(
        className="aux", 
        children=[
            dcc.Interval(
                id="aux-interval-3000", 
                interval=3*1000,
            ),
            dcc.Interval(
                id='periodic-check-scroll-position', 
                interval=1000
            ),
            dcc.Store(id='fig-scroll-data'),
            dcc.Store(id='fig-chapter-locations'),
            html.Div(id='chapter-position-json', children=""),
            # dcc.Store(id='fig-graph-aspect-ratio', data={"aspect_ratio":1.0}),
            # html.Div(id='fig-graph-aspect-ratio'),
            html.Div(id='fig-graph-aspect-ratio', children="1.0"),
        ],
        style={"display":"none"},
    )
    
    return aux