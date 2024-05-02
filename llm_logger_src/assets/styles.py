################################################################################
##                                LAYOUT STYLE                                ##
################################################################################
LAYOUT_STYLES = dict(
    default = dict(
            # plot_bgcolor='honeydew',
            # paper_bgcolor='honeydew',
            autosize=False,  # Disables automatic resizing based on the container
            
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
    ),
)


################################################################################
##                                 XAXES STYLE                                ##
################################################################################
XAXES_STYLES = dict(
    default = dict(
        # mirror=False,
        # nticks=0,
        # ticks="",
        # showgrid=False, 
        # showline=False,
        # zeroline=False, 
        # showticklabels=False,
        
        # fixedrange=True, 
        # range=(0, 1),
        # autorange=False,
        # constrain="domain",
        # rangemode="nonnegative",
        
        fixedrange=True,  # Prevents zooming and panning
        range=[0, 1],     # Explicitly setting the range from 0 to 1
        autorange=False   # Ensures that autorange is turned off
    ),
)

################################################################################
##                                 YAXES STYLE                                ##
################################################################################
YAXES_STYLES = dict(
    default = dict(
        # mirror=False,
        # nticks=0,
        # ticks="",
        # showgrid=False, 
        # showline=False,
        # zeroline=False, 
        # showticklabels=False, 
        
        autorange='reversed',
        scaleanchor="x",
        scaleratio=1,
        # rangemode="tozero",
    ),
)


################################################################################
##                             ANNOTATIONS STYLE                              ##
################################################################################
# annotations=[
#     dict(
#             showarrow=False,
#             xref="paper", 
#             yref="paper",
#             x=0.005, 
#             y=-0.002,
#         )
#     ],


################################################################################
##                                COLUMN STYLE                                ##
################################################################################
COLUMN_STYLES = dict(
    default = dict(
        fillcolor='green',
        opacity=0.1,
        line_width=0,
        layer="below",
    ),
)


################################################################################
##                                  NODE STYLE                                ##
################################################################################
NODE_STYLES = dict(
    default = dict(
            fillcolor='blue',
            # fillpattern = dict(
            #     fgcolor='green', 
            #     fillmode='replace', 
            #     shape="x",
            #     ),
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
CHAPTER_STYLES = dict(
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


################################################################################
##                                  EDGE STYLE                                ##
################################################################################
EDGE_STYLES = dict(
    default = dict(
            line = dict(width=3.0, color='blue'),
            mode = "lines",
        ),
)