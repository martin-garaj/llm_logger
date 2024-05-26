from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import html, dcc
import json
import base64
import io

from llm_logger_src.llm_logger import LLMLogger
from llm_logger_src.llm_parser import LLMLogParser
import pathlib as pl
from typing import Dict, List
import networkx as nx
from plotly import graph_objects as go


def __get_graph_element(parser:LLMLogParser) -> dcc.Graph:
    figure = parser.render_figure()
    graph_element = dcc.Graph(
        id="fig-graph", 
        className="fig-graph", 
        figure = figure,
        config=dict(
            autosizable=False,
            responsive=False,
        ),
    )
    return graph_element


def __get_chapter_locations(parser:LLMLogParser) -> Dict[str, list]:
    chapter_locations = parser.chapters
    chapter_locations["scrollRelative"] = chapter_locations["y"] / chapter_locations["y"].max() 
    chapter_locations["scrollAbsolute"] = chapter_locations["y"]
    chapter_locations.drop(columns = ["x", "y"], inplace=True)
    chapter_locations = chapter_locations.to_dict("list")
    return chapter_locations

def __get_chapter_buttons(parser:LLMLogParser) -> List[html.Div]:
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
    return chapter_buttons


def __get_related_traces(parser:LLMLogParser) -> Dict[str, List[str]]:
    # related traces (NOTICE, type is <str> because dcc.Store changes keys to <str>)
    temp_related_traces = parser.related_traces
    related_traces = dict()
    for index, related_indices in temp_related_traces.items():
        related_traces[str(index)] = [str(index) for index in related_indices]
    return related_traces


def __get_example_graph() -> nx.Graph:
    logger = LLMLogger()
    graph=logger._test(
        num_nodes=50, 
        num_chapters=4, 
        num_columns=4, 
        connectivity=0.9,
        )
    return graph


def __decode_file_to_graph(content_string, filename) -> nx.Graph:
    decoded = base64.b64decode(content_string)
    file_like = io.BytesIO(decoded)
    logger = LLMLogger()
    graph = logger.load(path_or_buffer=file_like, filename=filename)
    return graph


def register_render_graph(app):
    @app.callback(
        [Output('fig-plotly', 'children'),
         Output('fig-chapter-locations', 'data'),
         Output('fig-index', 'children'),
         Output('fig-graph-aspect-ratio', 'children'),
         Output('fig-related-traces', 'data'),
         Output('fig-node-styles', 'data'),
         Output('fig-chapter-styles', 'data'),
         Output('fig-edge-styles', 'data'),
         Output('fig-title-file', 'children')
        ],
        [Input('upload-file', 'contents'),
         State('upload-file', 'filename'),
         State('upload-file', 'last_modified')
         ]
    )
    def render_graph(contents, filename, last_modified):
        
        print(f"serverside callback -> render_graph -> {last_modified}")
        
        if contents is None:
            graph = __get_example_graph()
            filename = "<example graph>"
        else:
            content_type, content_string = contents.split(',')
            graph = __decode_file_to_graph(
                    content_string=content_string, 
                    filename=filename,
                )

        parser = LLMLogParser(graph=graph)
        
        # DEBUG purpose only
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
        
        graph_element = __get_graph_element(parser)
        chapter_locations = __get_chapter_locations(parser)
        chapter_buttons = __get_chapter_buttons(parser)
        aspect_ratio = f"{parser.aspect_ratio:.3f}"
        related_traces = __get_related_traces(parser)
        node_styles = parser.node_styles
        chapter_styles = parser.chapter_styles
        edge_styles = parser.edge_styles
        fig_title_file = [filename]
        
        return graph_element, \
            chapter_locations, \
            chapter_buttons, \
            aspect_ratio, \
            related_traces, \
            node_styles, \
            chapter_styles, \
            edge_styles, \
            fig_title_file






# def register_render_test_figure(app):
#     @app.callback(
#         [Output('fig-graph', 'figure'),
#          Output('fig-chapter-locations', 'data'),
#          Output('fig-index', 'children'),
#          Output('fig-graph-aspect-ratio', 'children'),
#          Output('fig-related-traces', 'data'),
#          Output('fig-node-styles', 'data'),
#          Output('fig-chapter-styles', 'data'),
#          Output('fig-edge-styles', 'data'),
#         ],
#         Input('fig-graph', 'id'),
#     )
#     def render_test_figure(trigger):
#         print(f"running render_test_figure()")
#         if not trigger:
#             raise PreventUpdate  # Prevents the callback from firing if the trigger is somehow None or invalid

#         print(f"running render_test_figure() -> executing ...")
        
#         # Create the figure to be displayed
#         logger = LLMLogger(
#             path=pl.Path('./'),
#             file='test_log.json',
#         )
#         # graph=logger._test(num_nodes=100, num_chapters=10, num_columns=4, connectivity=0.2)
#         # graph=logger._test(num_nodes=5, num_chapters=2, num_columns=4, connectivity=0.2)
#         graph=logger._test(num_nodes=50, num_chapters=4, num_columns=4, connectivity=0.9)
        
#         parser = LLMLogParser(graph=graph)
#         figure = parser.render_figure()
#         parser.report(
#             column_order=False, 
#             column_positions=False, 
#             vertex_positions=False, 
#             partitioned_vertices=False,
#             partitioned_edges=False,
#             partitioned_traces=True,
#             partitions=False,
#             related_traces=True,
#             chapters=True,
#             figure=False,
#         )
#         # get chapters
#         chapter_locations = parser.chapters
#         chapter_locations["scrollRelative"] = chapter_locations["y"] / chapter_locations["y"].max() 
#         chapter_locations["scrollAbsolute"] = chapter_locations["y"]
#         chapter_locations.drop(columns = ["x", "y"], inplace=True)
#         chapter_locations = chapter_locations.to_dict("list")
        
        
#         chapter_buttons = list()
#         for row in parser.chapters.itertuples():
#             if row.Index == 0:
#                 chapter_name = f"α"
#             elif row.Index == parser.chapters.index[-1]:
#                 chapter_name = f"ω"
#             else:
#                 chapter_name = f"{int(row.Index)}"
            
#             chapter_buttons.append(
#                 html.Div(
#                     id={"type": "fig-chapter-button", "index": int(row.Index)}, 
#                     children=[chapter_name],  
#                     className="fig-chapter",
#                     **{ 'data-index': int(row.Index), 
#                         'data-type': 'fig-chapter-button', 
#                         'data-chapter-id': row.id,
#                         },
#                     ),
#                 )
        
#         # aspect ratio 
#         aspect_ratio = f"{parser.aspect_ratio:.3f}"
        
#         # related traces (NOTICE, type is <str> because dcc.Store changes keys to <str>)
#         temp_related_traces = parser.related_traces
#         related_traces = dict()
#         for index, related_indices in temp_related_traces.items():
#             related_traces[str(index)] = [str(index) for index in related_indices]
        
        
#         # styles - parser assures the styles are consistent
#         node_styles = parser.node_styles
#         chapter_styles = parser.chapter_styles
#         edge_styles = parser.edge_styles
        
#         print(f"running render_test_figure() -> ... finished!")
        
#         return figure, chapter_locations, chapter_buttons, aspect_ratio, related_traces, node_styles, chapter_styles, edge_styles


def register_update_positions_json(app):
    @app.callback(
        Output('fig-chapter-locations-json', 'children'),
        Input('fig-chapter-locations', 'data')
    )
    def update_positions_json(positions):
        # print(json.dumps(positions))
        return json.dumps(positions)
    
