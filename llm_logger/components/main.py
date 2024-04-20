from dash import html

try:
    from llm_logger.components.figure import figure
    from llm_logger.components.display import display
except ImportError:
    from .figure import figure
    from .display import display



main_left = html.Div(
    id="main-left",
    className="main-left",
    children=[figure()],
)

main_right = html.Div(
    id="main-right",
    className="main-right",
    children=[display()],
)

def main() -> html.Div:
    main_div = html.Div(
        id="main",
        className="main-content",
        children=[
            main_left,
            main_right,
        ],
    )
    
    return main_div