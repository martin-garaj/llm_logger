################################################################################
##                                LAYOUT STYLE                                ##
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


################################################################################
##                                 XAXES STYLE                                ##
################################################################################
XAXES_DEFAULT_STYLE = dict(
    mirror=False,
    nticks=0,
    ticks="",
    showline=False,
    zeroline=False,
)


################################################################################
##                                 YAXES STYLE                                ##
################################################################################
YAXES_DEFAULT_STYLE = dict(
    mirror=False,
    nticks=0,
    ticks="",
    showline=False,
    zeroline=False,
    scaleanchor="x",
)


################################################################################
##                                  NODE STYLE                                ##
################################################################################
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

################################################################################
##                                CHAPTER STYLE                               ##
################################################################################
CHAPTER_DEFAULT_STYLES = dict(
    default = dict(
            fillcolor='darkorange',
            line = dict(width=3.0, color='darkslategray'),
            mode="lines",
        ),
    __start__ = dict(
            fillcolor='red',
            line = dict(width=3.0, color='darkslategray'),
            mode="lines",
        ),
    __end__ = dict(
            fillcolor='green',
            line = dict(width=3.0, color='darkslategray'),
            mode="lines",
        ),
)