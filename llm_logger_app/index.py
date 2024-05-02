"""
export PYTHONPATH="${PYTHONPATH}:/home/gartin/Documents/AlphaPrompt/Fairy_tales/Projects/llm_logger/llm_logger"

lsof -i :8050
kill -9 <PID>
"""

################################################################################
##                               special imports                              ##
################################################################################
if __name__ == '__main__':
    import sys
    import os
    import pathlib as pl
    project_root = pl.Path(os.getcwd()).absolute()
    # project_src = pl.Path(project_root, 'llm_logger', 'llm_logger_src')
    # project_app = pl.Path(project_root, 'llm_logger', 'llm_logger_app')
    project_src = pl.Path(project_root, 'llm_logger_src')
    project_app = pl.Path(project_root, 'llm_logger_app')
    
    
    for path_to_add in [project_root, project_app, project_src]:
        if not path_to_add.exists():
            raise RuntimeError(f"path='{path_to_add}' does not exist!")
        try:
            sys.path.index(str(path_to_add))
        except ValueError:
            sys.path.append(str(path_to_add))
        print(f"->   PYTHONPATH now includes '{path_to_add}'")
    # project_root_in_sys = sys.path[sys.path.index(project_root)]
    # print(f"TESTING: add '{project_root_in_sys}' to PYTHONPATH")


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
    from llm_logger_app.components.aux import aux
    
    from llm_logger_app.callbacks.options_open import register_options_open
    from llm_logger_app.callbacks.theme_change import register_theme_change
    from llm_logger_app.callbacks.plotly_figure import register_render_test_figure
    from llm_logger_app.callbacks.select_node import register_select_node
    from llm_logger_app.callbacks.store_report import register_store_report
    
except ImportError:
    from components.header import header
    from components.options import options
    from components.footer import footer
    from components.main import main
    from components.aux import aux
    
    from callbacks.options_open import register_options_open
    from callbacks.theme_change import register_theme_change
    from callbacks.plotly_figure import register_render_test_figure
    from callbacks.select_node import register_select_node
    from callbacks.store_report import register_store_report


app.layout = html.Div(
    id="app",
    className="app",
    children=[
        options(initial_theme=initial_theme, 
                available_themes=available_themes),
        header(),
        main(),
        footer(),
        aux(),
        ],
    **{"data-theme": initial_theme},
)

################################################################################
##                                  callbacks                                 ##
################################################################################
try:
    from llm_logger_app.callbacks.options_open import register_options_open
    from llm_logger_app.callbacks.theme_change import register_theme_change
    from llm_logger_app.callbacks.plotly_figure import \
        register_render_test_figure, register_resize_figure
    from llm_logger_app.callbacks.clientside.fig_scroll_data import \
        register_fig_scroll_data
except ImportError:
    from callbacks.options_open import register_options_open
    from callbacks.theme_change import register_theme_change
    from callbacks.plotly_figure import register_render_test_figure
    from callbacks.plotly_figure import register_resize_figure
    from callbacks.clientside.fig_scroll_data import register_fig_scroll_data

register_options_open(app)
register_theme_change(app)
register_render_test_figure(app)
register_select_node(app)

# register_resize_figure(app)

register_store_report(app)

# clientside
register_fig_scroll_data(app)

from dash import ClientsideFunction, Input, Output

# app.clientside_callback(
#     ClientsideFunction(
#         namespace='clientside',
#         function_name='getScrollData'
#     ),
#     Output('fig-scroll-data', 'data'),
#     Input('periodic-check-scroll-position', 'n_intervals')
# )


################################################################################
##                                 run server                                 ##
################################################################################
if __name__ == '__main__':
    
    app.run_server(debug=False)
