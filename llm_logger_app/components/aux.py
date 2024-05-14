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
                interval=1000,
            ),
            dcc.Store(id='fig-scroll-data'),
            dcc.Store(id='fig-chapter-locations'),
            dcc.Store(id='fig-related-traces'),
            dcc.Store(id='fig-node-styles'),
            dcc.Store(id='fig-edge-styles'),
            dcc.Store(id='fig-chapter-styles'),
            
            html.Div(id='fig-chapter-locations-json', children=""),
            html.Div(id='fig-graph-aspect-ratio', children="1.0"),
        ],
        style={"display":"none"},
    )
    
    return aux