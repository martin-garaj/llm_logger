from dash import html
    
# try:
#     from llm_logger.constants import ID
# except ImportError:
#     from .constants import ID
# from llm_logger.constants import ID

################################################################################
##                                   bar_top                                  ##
################################################################################
def button(style:dict, ) -> html.Div:
    """ Defines the main UI of the logger.
    """
    button = html.Div(
        id="btn",
        children=[html.Div(),
                  ],
        style=style,
    )
    return button


if __name__ == '__main__':
    from dash import html
    from dash import Dash

    app = Dash(__name__)

    def create_stylized_button(id, text):
        return html.Button(text, id=id, className='stylized-button')

    app.layout = html.Div([
        create_stylized_button('my-button', 'Click me!')
    ])
    app.run_server(debug=True)