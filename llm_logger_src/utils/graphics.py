from plotly import graph_objects as go
from typing import Dict, Any


def _get_node_trace(x:float, y:float, width:float, height:float, style:Dict[str, Any]) -> go.Scatter:

    top = y + (height/2)
    bottom = y - (height/2)
    left = x - (width/2)
    right = x + (width/2)

    trace = go.Scatter(
        x = [left, left, right, right, left],
        y = [top, bottom, bottom, top,  top],
        fill = "toself",
        **style,
    )
    
    return trace
    

################################################################################
##                                    TESTS                                   ##
################################################################################
if __name__ == "__main__":
    
    fig = go.Figure()
    
    fig.add_trace(
        _get_node_trace(
            x = 1.0,
            y = 2.0,
            width = 3.0,
            height = 1.0,
            style = dict(
                fillpattern = dict(fgcolor='red', fillmode='replace', shape="x"),
                line = dict(width=3.0, color='red'),
                mode = "lines",
            )
        )
        
    )
    
    # fig.update_xaxes(showgrid=False)
    fig.update_layout(
        yaxis = dict(autorange="reversed"),
        xaxis_range=[-4,4],
        yaxis_scaleanchor="x",
    )
    fig.show()
    