import dash
from dash import html

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    # Text field with formatted text
    html.Div(
        children=[
            html.Span("default "),
            html.Strong("text"),  # Bold text using Strong tag
            # You can add more text with additional formatting here
        ],
        style={
            'border': '1px solid #ccc',  # Thin border
            'border-radius': '5px',  # Rounded corners
            'background-color': '#f2f2f2',  # Gray background
            'padding': '10px',  # Some padding to avoid text touching the borders
            'margin': '10px',  # A bit of margin if needed
            'width': '100%',  # Takes the whole width of the page
            'height': '100vh',  # Takes the whole height of the viewport
            'box-sizing': 'border-box',  # Includes padding in the width and height
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
