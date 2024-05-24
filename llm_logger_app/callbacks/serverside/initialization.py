# from dash import Input, Output
# from dash.exceptions import PreventUpdate
# from dash import html
# import json

# from llm_logger_src.llm_logger import LLMLogger
# from llm_logger_src.llm_parser import LLMLogParser
# import pathlib as pl

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
        
