""" Example of a resizable layout using 3 buttons "33:67", "50:50", "67:33".

    The Plotly graph on the left preserves its scaling/zoom after the layout 
    is resized.
"""


import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the initial layout of the app
app.layout = html.Div([
    # Buttons for adjusting layout ratios
    html.Div([
        html.Button("33:67", id="btn-33", n_clicks=0),
        html.Button("50:50", id="btn-50", n_clicks=0),
        html.Button("67:33", id="btn-67", n_clicks=0)
    ], style={'padding': '10px'}),
    
    # Store component to keep the state of the graph
    dcc.Store(id='graph-store'),

    # Graph area - initially set with default layout
    dcc.Graph(
        id='my-graph',
        figure={
            'data': [go.Scatter(x=[], y=[], mode='lines')],
            'layout': go.Layout(title='Sin Wave', autosize=True, margin=dict(l=50, r=50, b=100, t=100, pad=4))
        },
        style={'width': '50%', 'height': '90vh', 'display': 'inline-block'},  # Default width
        config={'scrollZoom': True, 'displayModeBar': True}
    ),

    # Text window area - initially set with default layout
    html.Div(
        "Text associated with a node will appear here.",
        id='text-area',
        style={'width': '50%', 'display': 'inline-block', 'padding': '20px', 'overflowY': 'auto', 'height': '90vh'}  # Default width
    ),
])

@app.callback(
    [Output('my-graph', 'style'), Output('text-area', 'style'), Output('graph-store', 'data')],
    [Input("btn-33", "n_clicks"), Input("btn-50", "n_clicks"), Input("btn-67", "n_clicks")],
    [State('graph-store', 'data')],
)
def update_layout(btn_33, btn_50, btn_67, stored_data):
    # Determine which button was clicked
    ctx = dash.callback_context

    # Default layout ratio
    graph_width = 50
    text_width = 50

    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Update layout ratio based on the button clicked
        if button_id == "btn-33":
            graph_width = 33
            text_width = 67
        elif button_id == "btn-50":
            graph_width = 50
            text_width = 50
        elif button_id == "btn-67":
            graph_width = 67
            text_width = 33

    # Update styles for graph and text area based on the selected ratio
    graph_style = {'width': f'{graph_width}%', 'height': '90vh', 'display': 'inline-block'}
    text_style = {'width': f'{text_width}%', 'display': 'inline-block', 'padding': '20px', 'overflowY': 'auto', 'height': '90vh'}

    # No need to update the figure here, it will retain its state through dcc.Store
    return graph_style, text_style, stored_data

@app.callback(
    Output('graph-store', 'data', allow_duplicate=True),
    [Input('my-graph', 'relayoutData')],
    [State('graph-store', 'data')],
    prevent_initial_call=True
)
def store_graph_state(relayoutData, stored_data):
    if relayoutData and 'xaxis.range[0]' in relayoutData:
        # Update the stored layout with the new range
        new_layout = stored_data if stored_data else {}
        new_layout['xaxis'] = {'range': [relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']]}
        return new_layout
    return stored_data

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)