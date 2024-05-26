from dash import html, dcc
from plotly import graph_objects as go


def figure() -> html.Div:
    chapters = list()
    figure_div = html.Div(
                id="fig-content",
                className="fig-content",
                children=[ 
                    html.Div(id="fig-blank",  
                             className="fig-blank"),
                    html.Div(id="fig-title",  
                             className="fig-title", 
                            #  children=["Chapter title"],
                            children=[
                                html.Div(id="fig-title-file",
                                         className="fig-title-file", 
                                         children=["<filename>"],
                                ),
                                html.Div(id="fig-title-chapter",
                                         className="fig-title-chapter", 
                                         children=["Chapter title"],
                                ),
                            ]
                             ),
                    html.Div(id="fig-index",  
                             className="fig-index hide-scrollbar", 
                             children=chapters),
                    html.Div(id="fig-plotly", 
                             className="fig-plotly", 
                             children=[
                                 html.Div(id="fig-graph", \
                                     style={"display":"none"},
                                    )
                            #      dcc.Graph(
                            #     id="fig-graph", 
                            #     className="fig-graph", 
                            #     config=dict(
                            #         autosizable=False,
                            #         responsive=False,
                            #         ),
                            # ),
                                       ],
                             ),
                        ],
                )
    
    return figure_div





