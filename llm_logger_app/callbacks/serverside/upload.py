from datetime import datetime
from dash import html, Input, Output, State, ctx
import base64
import io
import pathlib

from dash import Input, Output, callback_context


def register_upload_open(app):
    @app.callback(
        Output("upload", "className"),
        [Input("button-open-upload", "n_clicks"), 
         Input("button-close-upload", "n_clicks")],
    )
    def upload_open(open_clicks, close_clicks):
        ctx = callback_context
        if not ctx.triggered:
            return "upload-closed"

        # Determine which button was clicked
        last_triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if last_triggered_id == 'button-open-upload':
            return "upload-opened"
        else:
            return "upload-closed"



# def register_upload_file(app):
#     @app.callback(
#         Output('display', 'children'),
#         Input('upload-file', 'contents'),
#         State('upload-file', 'filename'),
#         State('upload-file', 'last_modified')
#     )
#     def upload_file(contents, filename, date):
#         ## testing
#         if contents is not None:
#             children = [
#                 html.Div([
#                     html.Span(f'Filename: {filename}, Last Modified Date: {date}')
#                 ])
#             ]
            
#             if contents is not None:
#                 content_type, content_string = contents.split(',')
#                 decoded = base64.b64decode(content_string)
#                 filepath = pathlib.Path(ROOT, FOLDER_DATA, filename).resolve()
#                 print(f"callback -> server-side -> upload_file -> uploaded file : {filepath}")
#                 # with open(filepath, 'wb') as f:
#                 #     f.write(decoded)
#             else:
#                 print(f"'contents' empty!")
            
            
#             return children
        
#         return list()

