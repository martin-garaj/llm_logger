""" Example of dark mode including a Plotly figure.

    The figure changes color of the background when the dark mode is turned on.

"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the initial layout of the app
app.layout = html.Div([
    dcc.Graph(
        id='my-graph',
        figure={
            'data': [go.Scatter(x=[1, 2, 3], y=[4, 1, 2], fill='tozeroy')],
            'layout': go.Layout(
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='black')
            )
        }
    ),
    html.Div("default text with the word text in bold".replace("text", str(html.B("text"))), id='my-div'),
    html.Button("Light", id='light-button'),
    html.Button("Dark", id='dark-button'),
])

# Define the callback to update the styles based on button click
@app.callback(
    [Output('my-graph', 'figure'), Output('my-div', 'style')],
    [Input('light-button', 'n_clicks'), Input('dark-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_style(light_clicks, dark_clicks):
    # Get the id of the button that was clicked
    ctx = dash.callback_context

    if not ctx.triggered or ctx.triggered[0]['prop_id'] == 'light-button.n_clicks':
        # Light mode styles
        fig_bgcolor = 'white'
        paper_bgcolor = 'white'
        font_color = 'black'
        div_style = {'color': 'black', 'background-color': 'white'}
    else:
        # Dark mode styles
        fig_bgcolor = 'black'
        paper_bgcolor = 'black'
        font_color = 'white'
        div_style = {'color': 'white', 'background-color': 'black'}

    # Update the figure with the new styles
    fig = {
        'data': [go.Scatter(x=[1, 2, 3], y=[4, 1, 2], fill='tozeroy')],
        'layout': go.Layout(
            paper_bgcolor=paper_bgcolor,
            plot_bgcolor=fig_bgcolor,
            font=dict(color=font_color)
        )
    }

    return fig, div_style

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
