import dash
from dash import dcc, html, Input, Output, callback_context

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    # Button to open the options menu
    html.Button("Options", id="open-menu-button", n_clicks=0),
    
    # The sliding menu, initially hidden
    html.Div([
        # Button to close the menu
        html.Button("X", id="close-menu-button", n_clicks=0, style={'float': 'right'}),
        html.H2("Settings", style={'clear': 'both'}),
        
        # Menu buttons
        html.Button("A", id="button-a", n_clicks=0),
        html.Button("B", id="button-b", n_clicks=0),
        html.Button("C", id="button-c", n_clicks=0)
    ], id="sliding-menu", style={
        'display': 'none',  # Hidden by default
        'position': 'fixed',
        'top': 0, 'left': 0,
        'height': '33%', 'width': '100%',
        'background-color': 'rgba(255, 255, 255, 0.9)',  # Slightly transparent
        'z-index': 1000,  # Ensure it's above other content
        'text-align': 'center',
        'padding-top': '10px'
    }),
    
    # Application content
    html.Div("default text", id="app-content")
])

@app.callback(
    Output("sliding-menu", "style"),
    [Input("open-menu-button", "n_clicks"), Input("close-menu-button", "n_clicks")],
)
def toggle_menu(open_clicks, close_clicks):
    ctx = callback_context

    # If no buttons were clicked yet, keep the menu hidden
    if not ctx.triggered:
        return {'display': 'none'}

    # Determine which button was clicked
    last_triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # If the 'open-menu-button' was clicked, show the menu, else hide it
    if last_triggered_id == 'open-menu-button':
        return {
            'position': 'fixed',
            'top': 0, 'left': 0,
            'height': '33%', 'width': '100%',
            'background-color': 'rgba(99, 99, 99, 0.5)',
            'z-index': 1000,
            'text-align': 'center',
            'padding-top': '10px',
            'display': 'block'  # Show the menu
        }
    else:  # This would be 'close-menu-button' or any other close trigger
        return {'display': 'none'}  # Hide the menu

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
