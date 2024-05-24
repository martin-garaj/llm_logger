from dash import Input, Output, callback_context

def register_options_open(app):
    @app.callback(
        Output("options", "className"),
        [Input("button-open-options", "n_clicks"), 
         Input("button-close-options", "n_clicks")],
    )
    def options_open(open_clicks, close_clicks):
        ctx = callback_context

        # If no buttons were clicked yet, keep the menu hidden
        if not ctx.triggered:
            return "options-closed"

        # Determine which button was clicked
        last_triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # If the 'open-menu-button' was clicked, show the menu, else hide it
        if last_triggered_id == 'button-open-options':
            return "options-opened"
        else:  # This would be 'close-menu-button' or any other close trigger
            return "options-closed"