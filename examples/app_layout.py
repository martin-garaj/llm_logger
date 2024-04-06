import dash
from dash import html

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    # Top bar with buttons
    html.Div([
        html.Button('btn-input', style={'display': 'inline-block', 'margin': '1em'}),
        html.Div('bar-top', style={'display': 'inline-block', 'margin-left': '20em', 'margin-right': '20em'}),
        html.Button('btn-settings', style={'display': 'inline-block', 'margin': '1em'}),
    ], style={'text-align': 'center'}),
    
    # Main content area
    html.Div([
        # Left section
        html.Div([
            html.Div('display-section', style={
                'border': '1px solid black', 'margin-bottom': '-1em',  # Protrudes over the display-figure
                'padding': '1em'
            }),
            html.Div('display-figure', style={
                'border': '1px solid black', 'padding': '1em'
            }),
            html.Button('btn-section', style={'margin-top': '1em'}),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '1em'}),
        
        # Right section
        html.Div([
            html.Div('display-text', style={
                'border': '1px solid black', 'padding': '1em', 'margin-bottom': '1em'
            }),
            html.Div([
                html.Button('btn-text', style={'margin-right': '1em'}),
                html.Button('btn-html'),
            ], style={'text-align': 'center'}),
        ], style={'display': 'inline-block', 'vertical-align': 'top'}),
    ]),
    
    # Bottom bar
    html.Div('bar-bottom', style={'text-align': 'center', 'margin-top': '1em'}),
], style={'width': '100%', 'font-size': '1em'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)