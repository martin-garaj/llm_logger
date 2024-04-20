from dash import Input, Output, State, callback

def register_theme_change(app):

    @app.callback(
        [Output('app', 'data-theme'),
        Output('button-theme', 'children')],
        [Input('button-theme', 'n_clicks'),
        State('app', 'data-theme')],
        prevent_initial_call=True
    )
    def theme_change(n_clicks, data_theme):
        
        if n_clicks % 2:
            return 'dark', ["DARK"] 
        else:
            return 'light', ["LIGHT"]
