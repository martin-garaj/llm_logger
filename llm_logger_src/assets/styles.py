################################################################################
##                                DEFAULT STYLE                               ##
################################################################################
LAYOUT_DEFAULT_STYLE = dict(
            plot_bgcolor='honeydew',
            paper_bgcolor='honeydew',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=1, l=1, r=1, t=40),
            xaxis_showgrid=False, 
            yaxis_showgrid=False,
        )


XAXES_DEFAULT_STYLE = dict(
    mirror=False,
    nticks=0,
    ticks="",
    showline=False,
    zeroline=False,
)

YAXES_DEFAULT_STYLE = dict(
    mirror=False,
    nticks=0,
    ticks="",
    showline=False,
    zeroline=False,
    scaleanchor="x",
)


NODE_DEFAULT_STYLES = dict(
    default = dict(
            fillpattern = dict(
                fgcolor='green', 
                fillmode='replace', 
                shape="x",
                ),
            line = dict(width=3.0, color='red'),
            mode = "lines",
        ),
    decision = dict(
            fillcolor='blue',
            line = dict(width=3.0, color='green'),
            mode="lines",
        ),
    success = dict(
            fillcolor='limegreen',
            line = dict(width=3.0, color='green'),
            mode="lines",
        ),
    failure = dict(
            fillpattern = dict(
                fgcolor='red', 
                fillmode='replace', 
                shape="x"),
            line = dict(width=3.0, color='red'),
            mode = "lines",
        ),
)

CHAPTER_DEFAULT_STYLES = dict(
    default = dict(
            fillcolor='darkorange',
            line = dict(width=3.0, color='darkslategray'),
            mode="lines",
        ),

    extra = dict(
            fillcolor='gold',
            line = dict(width=3.0, color='darkslategray'),
            mode="lines",
        ),
)

################################################################################
##                                 DEFAULT 1                                  ##
################################################################################
PLOT_STYLE_1 = dict(
    background = {
            "background-color":"darkgray",
        },
    column = {
            "background-color":"darkgray",
        },
)

NODE_STYLE_1 = dict(
    default = {
            "background-color":"gainsboro",
            "border-color":"black",
            "border-width":2,
        },
    decision = {
            "background-color":"darkturquoise",
            "border-color":"black",
            "border-width":2,
        },
    success = {
            "background-color":"limegreen",
            "border-color":"black",
            "border-width":2,
        },
    failure = {
            "background-color":"hotpink",
            "border-color":"black",
            "border-width":2,
        }
)

CHAPTER_STYLE_1 = dict(
    default = {
            "background-color":"chocolate",
            "border-color":"black",
            "border-width":2,
        },
    extra = {
            "background-color":"goldenrod",
            "border-color":"black",
            "border-width":2,
        },
)