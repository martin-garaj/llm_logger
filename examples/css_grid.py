from dash import html, Dash

app = Dash(
    __name__,
)

app.layout = html.Div([
    html.Div(id='grid-container', children=[
        html.Div('Top Cell', id='top-cell'),
        html.Div('Left Cell', id='left-cell'),
        html.Div('Right Cell', id='right-cell')
    ])
], style={'width': '50%', 'margin': 'auto'}) 


if __name__ == '__main__':

    app.run_server(debug=False)