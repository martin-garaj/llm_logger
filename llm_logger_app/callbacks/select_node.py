from dash import Input, Output
from dash.exceptions import PreventUpdate
from dash import html



def register_select_node(app):
    @app.callback(
        Output('display', 'children'),
        Input('display', 'id')
    )
    def select_node(trigger):

        lines = ["Ths is line 1",
         "",
         "sub_folders = [name for name in os.listdir(plotly_figure_path) if os.path.isdir(os.path.join(plotly_figure_path, name))]",
         "",
         "try:",
        "from llm_logger_app.callbacks.options_open import register_options_open",
        "from llm_logger_app.callbacks.theme_change import register_theme_change",
        "from llm_logger_app.callbacks.plotly_figure import",
        "    register_render_test_figure",
        "except ImportError:",
        "   from callbacks.options_open import register_options_open",
        "   from callbacks.theme_change import register_theme_change",
        "\tfrom callbacks.plotly_figure import register_render_test_figure",
        "",
        "register_options_open(app)",
        "register_theme_change(app)",
        "register_render_test_figure(app)",
         ]

        divs = list()

        divs.append(
            html.Div(
                children=[
                    html.Div(className="display-line-num"),
                    html.Div(className="display-line-text"),
                ],
                className="display-line display-start",
            )
        )

        for line_idx, line in enumerate(lines):
            divs.append(
                html.Div(
                    children=[
                        html.Div(children=f"{line_idx+1}", className="display-line-num"),
                        html.Div(children=f"{line}", className="display-line-text"),
                    ],
                    className="display-line"
                )
            )

        divs.append(
            html.Div(
                children=[
                    html.Div(className="display-line-num"),
                    html.Div(className="display-line-text"),
                ],
                className="display-line display-end",
            )
        )

        return divs
