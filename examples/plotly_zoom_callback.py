""" Example showing the Plotly graph to report the dimensions of the zoomed 
    section.
    
    This example can be used to obtain a feedback on zooming the Plotly graph 
    and updating other components accordingly. 

"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Sample data for the graph
x_values = list(range(100))  # X-axis values
y_values = [value ** 2 for value in x_values]  # Y-axis values, just as an example

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Graph(
        id='my-graph',
        figure={
            'data': [go.Scatter(x=x_values, y=y_values)],
            'layout': go.Layout(
                title='Scroll to Zoom and Pan',
                xaxis={'autorange': False, 'range': [0, 10]},  # Customize this range as needed
                yaxis={'autorange': True}
            )
        },
        config={'scrollZoom': True}  # Enable scroll zoom
    ),
    html.Div(id='graph-section-title', style={'padding': '20px', 'fontSize': '20px'})
])

# Define the callback to update the text based on scrolling/zooming
@app.callback(
    Output('graph-section-title', 'children'),
    Input('my-graph', 'relayoutData')
)
def update_text(relayoutData):
    if relayoutData and 'xaxis.range[0]' in relayoutData and 'xaxis.range[1]' in relayoutData:
        # Determine the current range of the x-axis
        x_start, x_end = relayoutData['xaxis.range[0]'], relayoutData['xaxis.range[1]']
        
        # Logic to determine the title based on the x-axis range
        # This is a simplified example. You might need a more sophisticated method
        # to determine the section based on the current x-axis range.
        section_title = f"Section: {x_start} to {x_end}"
        
        return section_title
    else:
        # Default text when the graph is first loaded or if there's no zoom/pan
        return "Scroll or zoom on the graph to see section titles"

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
