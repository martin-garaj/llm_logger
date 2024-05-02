from dash.dependencies import ClientsideFunction, Output, Input

def register_fig_scroll_data(app):
    app.clientside_callback(
        ClientsideFunction(
            namespace='clientside',
            function_name='getFigScrollData'
        ),
        Output('fig-scroll-data', 'data'),
        Input('periodic-check-scroll-position', 'n_intervals')
    )