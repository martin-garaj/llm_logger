"""
export PYTHONPATH="${PYTHONPATH}:/home/gartin/Documents/AlphaPrompt/Fairy_tales/Projects/llm_logger/llm_logger"

lsof -i :8050
kill -9 <PID>
"""
import os
import pandas as pd
from datetime import datetime
from dash import Dash, html, dcc, Input, Output
from typing import Dict
import pathlib

from options import FOLDER_DATA, FOLDER_METADATA, FILE_METADATA

################################################################################
##                                  DASH APP                                  ##
################################################################################
from dash import Dash

app = Dash(
    __name__,
    update_title=None,
    suppress_callback_exceptions=False,
)

################################################################################
##                               special imports                              ##
################################################################################
if __name__ == '__main__':
    import sys
    import os
    import pathlib as pl
    project_root = pl.Path(os.getcwd()).absolute()
    
    
    for path_to_add in [project_root]:
        if not path_to_add.exists():
            raise RuntimeError(f"path='{path_to_add}' does not exist!")
        try:
            sys.path.index(str(path_to_add))
        except ValueError:
            sys.path.append(str(path_to_add))
        print(f"->   PYTHONPATH now includes '{path_to_add}'")


################################################################################
##                               INITIALIZATION                               ##
################################################################################

ROOT = pl.Path(os.getcwd()).absolute()

if not os.path.exists(pl.Path(ROOT, FOLDER_DATA)):
    os.makedirs(pl.Path(ROOT, FOLDER_DATA))
print(f"->   data folder: {pl.Path(ROOT, FOLDER_DATA)}")

if not os.path.exists(pl.Path(ROOT, FOLDER_METADATA)):
    os.makedirs(pl.Path(ROOT, FOLDER_METADATA))
print(f"->   metadata folder: {pl.Path(ROOT, FOLDER_METADATA)}")

path_metadata_file = pl.Path(ROOT, FOLDER_METADATA, FILE_METADATA)
if not os.path.exists(path_metadata_file):
    df_metadata = pd.DataFrame(columns=['filename', 'upload_time', 'last_use_time', 'filepath'])
    df_metadata.to_csv(path_metadata_file, index=False)
else:
    df_metadata = pd.read_csv(path_metadata_file)

################################################################################
##                                   LAYOUT                                   ##
################################################################################
def upload() -> html.Div:
    
    upload_div = dcc.Upload(
            id='upload-file',
            className='upload-file',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            multiple=False,
            style_active={
                        'className': 'upload-file-active'
                    },
        )    
    
    div = html.Div(
        id="upload",
        className="upload", 
        children=[
            html.Div(
                id="upload-header",
                className="upload-header", 
                children=[
                    html.Div("", style={"flex-grow":"1"}),
                    html.Div("CLOSE", id="btn-close", className="button-generic"),
                    ],
            ),
            html.Div(
                id="upload-main",
                className="upload-main",
                children=[
                    html.Div(
                        className="upload-area", 
                        children=[upload_div], #"Drag and Drop or Select Files"
                    ),
                    html.Div(
                        className="btn-reload", 
                        children="RELOAD"
                    )
                ]      
            ),
            html.Div(children=[], id="display", className="display"),
        ]
    )
    
    return div


app.layout = html.Div(
    id="app",
    className="app",
    children=[
    upload(),
    html.Div(id='file-list')
])

################################################################################
##                            SERVER-SIDE CALLBACKS                           ##
################################################################################
import os
import pandas as pd
from datetime import datetime
from dash import Dash, html, dcc, Input, Output, State, ctx
import base64
import io

@app.callback(
    Output('display', 'children'),
    Input('upload-file', 'contents'),
    State('upload-file', 'filename'),
    State('upload-file', 'last_modified')
)
def update_output(contents, filename, date):
    ## testing
    if contents is not None:
        children = [
            html.Div([
                html.Span(f'Filename: {filename}, Last Modified Date: {date}')
            ])
        ]
        
        ## save file
        print(f"triggered 'update_output()' by id='{ctx.triggered_id}'")
        # if ctx.triggered_id == 'upload-file':
        print(f"'upload-file' element is the trigger")
        if contents is not None:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            filepath = pathlib.Path(ROOT, FOLDER_DATA, filename).resolve()
            # filepath = os.path.join(ROOT, FOLDER_DATA, filename)
            print(f"saving : {filepath}")
            # with open(filepath, 'wb') as f:
            #     f.write(decoded)
        else:
            print(f"'contents' empty!")
        
        
        return children
    
    return list()


################################################################################
##                                 RUN SERVER                                 ##
################################################################################
if __name__ == '__main__':
    
    app.run_server(
        debug=False,
        )
