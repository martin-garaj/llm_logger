from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

# Generate some data
x = np.linspace(0, 1, 100)
y = np.linspace(0, 100, 100)  # Large range for y to create a "tall" plot

fig = go.Figure(data=[go.Scatter(x=x, y=y)])
fig.update_layout(
    height=2000,  # Set a very tall height
    width=500,    # Set a reasonable width
    title="Scrollable Plot",
    xaxis_title="X Axis",
    yaxis_title="Y Axis",
    yaxis=dict(
        range=[0, 10]  # Initial visible range, user can zoom/pan to scroll
    ),
    margin=dict(t=50, l=50, b=50, r=50)
)

app.layout = html.Div([
    dcc.Graph(id='tall-plot', figure=fig),
    html.Div(id='output-range')
])

@app.callback(
    Output('output-range', 'children'),
    Input('tall-plot', 'relayoutData')
)
def display_visible_range(relayoutData):
    if relayoutData and 'yaxis.range[0]' in relayoutData and 'yaxis.range[1]' in relayoutData:
        return f"Currently viewing Y-axis from {relayoutData['yaxis.range[0]']:.2f} to {relayoutData['yaxis.range[1]']:.2f}"
    return "Adjust the plot to see Y-axis range."

if __name__ == '__main__':
    app.run_server(debug=True)