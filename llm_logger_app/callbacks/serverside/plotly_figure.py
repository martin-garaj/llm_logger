from dash import Input, Output
from dash.exceptions import PreventUpdate
from dash import html
import json

from llm_logger_src.llm_logger import LLMLogger
from llm_logger_src.llm_parser import LLMLogParser
import pathlib as pl

def register_render_test_figure(app):
    @app.callback(
        [Output('fig-graph', 'figure'),
         Output('fig-chapter-locations', 'data'),
         Output('fig-index', 'children'),
         Output('fig-graph-aspect-ratio', 'children'),
         Output('fig-related-traces', 'data'),
         Output('fig-node-styles', 'data'),
         Output('fig-chapter-styles', 'data'),
         Output('fig-edge-styles', 'data'),
        ],
        Input('fig-graph', 'id'),
    )
    def render_test_figure(trigger):
        print(f"running render_test_figure()")
        if not trigger:
            raise PreventUpdate  # Prevents the callback from firing if the trigger is somehow None or invalid

        print(f"running render_test_figure() -> executing ...")
        
        # Create the figure to be displayed
        logger = LLMLogger(
            path=pl.Path('./'),
            file='test_log.json',
        )
        # graph=logger._test(num_nodes=100, num_chapters=10, num_columns=4, connectivity=0.2)
        # graph=logger._test(num_nodes=5, num_chapters=2, num_columns=4, connectivity=0.2)
        graph=logger._test(num_nodes=50, num_chapters=4, num_columns=4, connectivity=0.9)
        
        parser = LLMLogParser(graph=graph)
        figure = parser.render_figure()
        parser.report(
            column_order=False, 
            column_positions=False, 
            vertex_positions=False, 
            partitioned_vertices=False,
            partitioned_edges=False,
            partitioned_traces=True,
            partitions=False,
            related_traces=True,
            chapters=True,
            figure=False,
        )
        # get chapters
        chapter_locations = parser.chapters
        chapter_locations["scrollRelative"] = chapter_locations["y"] / chapter_locations["y"].max() 
        chapter_locations["scrollAbsolute"] = chapter_locations["y"]
        chapter_locations.drop(columns = ["x", "y"], inplace=True)
        chapter_locations = chapter_locations.to_dict("list")
        
        
        chapter_buttons = list()
        for row in parser.chapters.itertuples():
            if row.Index == 0:
                chapter_name = f"α"
            elif row.Index == parser.chapters.index[-1]:
                chapter_name = f"ω"
            else:
                chapter_name = f"{int(row.Index)}"
            
            chapter_buttons.append(
                html.Div(
                    id={"type": "fig-chapter-button", "index": int(row.Index)}, 
                    children=[chapter_name],  
                    className="fig-chapter",
                    **{ 'data-index': int(row.Index), 
                        'data-type': 'fig-chapter-button', 
                        'data-chapter-id': row.id,
                        },
                    ),
                )
        
        # aspect ratio 
        aspect_ratio = f"{parser.aspect_ratio:.3f}"
        
        # related traces (NOTICE, type is <str> because dcc.Store changes keys to <str>)
        temp_related_traces = parser.related_traces
        related_traces = dict()
        for index, related_indices in temp_related_traces.items():
            related_traces[str(index)] = [str(index) for index in related_indices]
        
        
        # styles - parser assures the styles are consistent
        node_styles = parser.node_styles
        chapter_styles = parser.chapter_styles
        edge_styles = parser.edge_styles
        
        print(f"running render_test_figure() -> ... finished!")
        
        return figure, chapter_locations, chapter_buttons, aspect_ratio, related_traces, node_styles, chapter_styles, edge_styles


def register_update_positions_json(app):
    @app.callback(
        Output('fig-chapter-locations-json', 'children'),
        Input('fig-chapter-locations', 'data')
    )
    def update_positions_json(positions):
        # print(json.dumps(positions))
        return json.dumps(positions)
    

# from plotly import graph_objects as go

# def register_resize_figure(app):
# #     @app.callback(
# #     Output('responsive-graph', 'figure'),
# #     [Input('interval-component', 'n_intervals')],
# #     [State('responsive-graph', 'figure')]
# # )
# #     def update_graph(n, existing_figure):
# #         # Modify the figure to reset range - this is simplistic and should be adapted for actual data updates
# #         fig = go.Figure(existing_figure)
# #         fig.update_layout(xaxis=dict(range=[0.0, 1.0], fixedrange=True))
# #         return fig
    
#     @app.callback(
#         Output('fig-graph', 'figure', allow_duplicate=True),
#         [Input('aux-interval-5', 'n_intervals')],  # Assuming you have an Interval component that ticks on resize
#         [State('fig-graph', 'figure'),
#          State('fig-graph', 'relayoutData')],
#         prevent_initial_call=True,
#     )
#     def resize_figure(n, figure, relayoutData):
        
#         print(relayoutData)
#         if relayoutData and 'yaxis.range[0]' in relayoutData and 'yaxis.range[1]' in relayoutData:
#             # Determine the current range of the x-axis
#             y_start, y_end = relayoutData['yaxis.range[0]'], relayoutData['yaxis.range[1]']
#             print(f"y_start = {y_start:0.1f}    y_end = {y_end:0.1f}")
#         fig = go.Figure(figure)
#         # fig.update_layout(
#         #     # width=None,  # Resetting width and height so it can autosize
#         #     # height=None
#         #     xaxis=dict(range:[0.0, 1.0])
#         # )
#         # fig.update_yaxes(
#         #     autorange='reversed',
#         #     scaleanchor="x",
#         #     scaleratio=1,
#         # )
#         fig.update_xaxes(
#             fixedrange=True,  # Prevents zooming and panning
#             range=[0, 1],     # Explicitly setting the range from 0 to 1
#             autorange=False   # Ensures that autorange is turned off
#         )

#         print(f"aux-interval-5 fired")
#         return fig
    
