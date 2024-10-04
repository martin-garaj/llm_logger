"""
export PYTHONPATH="${PYTHONPATH}:<path>/llm_logger"

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
##                               INITIALIZATION                               ##
################################################################################
initial_theme = 'light'
available_themes = dict(
    light="LIGHT",
    dark="DARK"
)


################################################################################
##                                  DASH APP                                  ##
################################################################################
from dash import Dash

app = Dash(
    __name__,
    update_title=None,
    suppress_callback_exceptions=True,
)


################################################################################
##                                   LAYOUT                                   ##
################################################################################
from dash import html

try:
    from llm_logger_app.components.header import header
    from llm_logger_app.components.options import options
    from llm_logger_app.components.footer import footer
    from llm_logger_app.components.main import main
    from llm_logger_app.components.aux import aux
    from llm_logger_app.components.upload import upload
except ImportError:
    from components.header import header
    from components.options import options
    from components.footer import footer
    from components.main import main
    from components.aux import aux
    from components.upload import upload
    

app.layout = html.Div(
    id="app",
    className="app",
    children=[
            header(),
            main(),
            footer(),
            aux(),
            options(
                initial_theme=initial_theme, 
                available_themes=available_themes),
            upload(),
        ],
    **{"data-theme": initial_theme},
)


################################################################################
##                            SERVER-SIDE CALLBACKS                           ##
################################################################################
try:
    from llm_logger_app.callbacks.serverside.options import \
        register_options_open
    from llm_logger_app.callbacks.serverside.upload import \
        register_upload_open
    from llm_logger_app.callbacks.serverside.theme_change import \
        register_theme_change
    from llm_logger_app.callbacks.serverside.plotly_figure import \
        register_render_graph, register_update_positions_json
    from llm_logger_app.callbacks.serverside.display_trace_content import \
        register_display_trace_content
    from llm_logger_app.callbacks.serverside.fig_highlight_traces import \
        register_fig_highlight_traces
    from llm_logger_app.callbacks.serverside.store_report import \
        register_store_report
except ImportError:
    from callbacks.serverside.options import register_options_open
    from callbacks.serverside.upload import register_upload_open
    from callbacks.serverside.theme_change import register_theme_change
    from callbacks.serverside.plotly_figure import \
        register_render_graph, register_update_positions_json
    from callbacks.serverside.display_trace_content import \
        register_display_trace_content
    from callbacks.serverside.fig_highlight_traces import \
        register_fig_highlight_traces
    from callbacks.serverside.store_report import register_store_report

register_options_open(app)
register_upload_open(app)
register_theme_change(app)
register_render_graph(app)
register_display_trace_content(app)
register_fig_highlight_traces(app)

register_store_report(app)


################################################################################
##                            CLIENT-SIDE CALLBACKS                           ##
################################################################################
try:
    from llm_logger_app.callbacks.clientside.fig_scroll_data import register_fig_scroll_data
except ImportError:
    from callbacks.clientside.fig_scroll_data import register_fig_scroll_data

register_fig_scroll_data(app)
register_update_positions_json(app)


################################################################################
##                                 RUN SERVER                                 ##
################################################################################
if __name__ == '__main__':
    
    app.run_server(
        debug=False,
        )
