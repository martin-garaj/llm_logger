
from dash import html, dcc


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
    
    upload_menu_div = html.Div(
        id="upload",
        className="upload-closed", 
        children=[
            html.Div(
                id="upload-header",
                className="upload-header", 
                children=[
                    html.Div("", style={"flex-grow":"1"}),
                    html.Div(
                        "CLOSE", 
                        id="button-close-upload", 
                        className="button-generic"),
                    ],
            ),
            html.Div(
                id="upload-main",
                className="upload-main",
                children=[
                    html.Div(
                        className="upload-area", 
                        children=[upload_div],
                    ),
                    html.Div(
                        className="button-reload-upload", 
                        children="RELOAD"
                    ),
                ],
            ),
            # html.Div(
            #     children=[], 
            #     id="display", 
            #     className="display"),
        ]
    )
    
    return upload_menu_div