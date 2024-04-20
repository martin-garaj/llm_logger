"""
export PYTHONPATH="${PYTHONPATH}:/home/gartin/Documents/AlphaPrompt/Fairy_tales/Projects/llm_logger/llm_logger"

lsof -i :8050
kill -9 <PID>
"""

################################################################################
##                               initialization                               ##
################################################################################
initial_theme = 'light'
available_themes = dict(
    light="LIGHT",
    dark="DARK"
)


################################################################################
##                                  dash app                                  ##
################################################################################
from dash import Dash

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
)


################################################################################
##                                   layout                                   ##
################################################################################
from dash import html

try:
    from llm_logger_app.components.header import header
    from llm_logger_app.components.options import options
    from llm_logger_app.components.footer import footer
    from llm_logger_app.components.main import main
except ImportError:
    from components.header import header
    from components.options import options
    from components.footer import footer
    from components.main import main


app.layout = html.Div(
    id="app",
    className="app",
    children=[
        options(initial_theme=initial_theme, 
                available_themes=available_themes),
        header(),
        main(),
        footer()],
    **{"data-theme": initial_theme},
)


################################################################################
##                                  callbacks                                 ##
################################################################################
try:
    from llm_logger_app.callbacks.options_open import register_options_open
    from llm_logger_app.callbacks.theme_change import register_theme_change
except ImportError:
    from callbacks.options_open import register_options_open
    from callbacks.theme_change import register_theme_change

register_options_open(app)
register_theme_change(app)


################################################################################
##                                 run server                                 ##
################################################################################
if __name__ == '__main__':
    from dash import html
    from dash import Dash

    app.run_server(debug=False)
