from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from llm_logger_src.llm_logger import LLMLogger
from llm_logger_src.llm_parser import LLMLogParser
import pathlib as pl

def register_render_test_figure(app):
    @app.callback(
        [Output('fig-graph', 'figure'),
         Output('fig-chapter-locations', 'data'),
        ],
        Input('fig-graph', 'id'),
    )
    def render_test_figure(trigger):
        print(f"running render_test_figure()")
        if not trigger:
            raise PreventUpdate  # Prevents the callback from firing if the trigger is somehow None or invalid

        print(f"running render_test_figure() ... executing")
        
        # Create the figure to be displayed
        logger = LLMLogger(
            path=pl.Path('./'),
            file='test_log.json',
        )
        graph=logger._test()
        
        logger.report()
        
        parser = LLMLogParser(graph=graph)
        parser.report()
        figure = parser.render_figure(column_style=None)
        # get chapters
        chapter_locations = parser.chapters
        chapter_locations["scroll"] = chapter_locations["y"] / chapter_locations["y"].max() 
        chapter_locations.drop(columns = ["x", "y"], inplace=True)
        chapter_locations = chapter_locations.to_dict("list")
        
        return figure, chapter_locations



from plotly import graph_objects as go

def register_resize_figure(app):
#     @app.callback(
#     Output('responsive-graph', 'figure'),
#     [Input('interval-component', 'n_intervals')],
#     [State('responsive-graph', 'figure')]
# )
#     def update_graph(n, existing_figure):
#         # Modify the figure to reset range - this is simplistic and should be adapted for actual data updates
#         fig = go.Figure(existing_figure)
#         fig.update_layout(xaxis=dict(range=[0.0, 1.0], fixedrange=True))
#         return fig
    
    @app.callback(
        Output('fig-graph', 'figure', allow_duplicate=True),
        [Input('aux-interval-5', 'n_intervals')],  # Assuming you have an Interval component that ticks on resize
        [State('fig-graph', 'figure'),
         State('fig-graph', 'relayoutData')],
        prevent_initial_call=True,
    )
    def resize_figure(n, figure, relayoutData):
        
        print(relayoutData)
        if relayoutData and 'yaxis.range[0]' in relayoutData and 'yaxis.range[1]' in relayoutData:
            # Determine the current range of the x-axis
            y_start, y_end = relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']
            print(f"y_start = {y_start:0.1f}    y_end = {y_end:0.1f}")
        fig = go.Figure(figure)
        # fig.update_layout(
        #     # width=None,  # Resetting width and height so it can autosize
        #     # height=None
        #     xaxis=dict(range:[0.0, 1.0])
        # )
        # fig.update_yaxes(
        #     autorange='reversed',
        #     scaleanchor="x",
        #     scaleratio=1,
        # )
        fig.update_xaxes(
            fixedrange=True,  # Prevents zooming and panning
            range=[0, 1],     # Explicitly setting the range from 0 to 1
            autorange=False   # Ensures that autorange is turned off
        )

        print(f"aux-interval-5 fired")
        return fig
    
