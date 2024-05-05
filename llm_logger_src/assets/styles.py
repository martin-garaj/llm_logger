################################################################################
##                              NODE ANNOTATIONS                              ##
################################################################################
# Available variables:
#   https://plotly.com/python/reference/layout/annotations/#layout-annotations-items-annotation-captureevents
#
# Not available (pre-set within code to prevent user interference):
#   captureevents
#   showarrow
NODE_ANNOTATIONS = dict(
    default = dict(
            font=dict(
                family="monospace",
                size=12,
                color="white",
            ),
            align = "center",
    ),
    __default__ = dict(
            font=dict(
                family="monospace",
                size=12,
                color="white",
            ),
            align = "center",
    ),
)

################################################################################
##                             CHAPTER ANNOTATIONS                            ##
################################################################################
# Available variables:
#   https://plotly.com/python/reference/layout/annotations/#layout-annotations-items-annotation-captureevents
#
# Not available (pre-set within code to prevent user interference):
#   captureevents
#   showarrow
CHAPTER_ANNOTATIONS = dict(
    default = dict(
            font=dict(
                family="monospace",
                size=16,
                color="white",
            ),
            align = "center",
    ),
    __start__ = dict(
            font=dict(
                family="monospace",
                size=16,
                color="white",
            ),
            align = "center",
        ),
    __end__ = dict(
            font=dict(
                family="monospace",
                size=16,
                color="white",
            ),
            align = "center",
        ),
    __default__ = dict(
            font=dict(
                family="monospace",
                size=16,
                color="white",
            ),
            align = "center",
    ),
)



################################################################################
##                                LAYOUT STYLE                                ##
################################################################################
LAYOUT_STYLES = dict(
    __default__ = dict(
            plot_bgcolor='azure',
            paper_bgcolor='azure',
            autosize=True,  # Disables automatic resizing based on the container
            
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
    ),
)


################################################################################
##                                 XAXES STYLE                                ##
################################################################################
XAXES_STYLES = dict(
    __default__ = dict(
        mirror=False,
        nticks=0,
        ticks="",
        showgrid=False, 
        showline=False,
        zeroline=False, 
        showticklabels=False,
        
        fixedrange=True, 
        range=[0.0, 1.0],
        autorange=False,
        constrain="domain",
        # rangemode="nonnegative",
    ),
)

################################################################################
##                                 YAXES STYLE                                ##
################################################################################
YAXES_STYLES = dict(
    __default__ = dict(
        mirror=False,
        nticks=0,
        ticks="",
        showgrid=False, 
        showline=False,
        zeroline=False, 
        showticklabels=False, 
        
        autorange='reversed',
        scaleanchor="x",
        scaleratio=1,
        # rangemode="tozero",
    ),
)


################################################################################
##                                COLUMN STYLE                                ##
################################################################################
COLUMN_STYLES = dict(
    __default__ = dict(
        fillcolor='gainsboro',
        opacity=0.9,
        line_width=0,
        layer="below",
    ),
)


################################################################################
##                                  NODE STYLE                                ##
################################################################################
NODE_STYLES = dict(
    default = dict(
            fillcolor='dodgerblue',
            line = dict(width=2.0, color='black'),
            mode = "lines",
        ),
    decision = dict(
            fillcolor='mediumvioletred',
            line = dict(width=2.0, color='black'),
            mode = "lines",
        ),
    success = dict(
            fillcolor='seagreen',
            line = dict(width=2.0, color='black'),
            mode = "lines",
        ),
    failure = dict(
            fillcolor='orangered',
            line = dict(width=2.0, color='black'),
            mode = "lines",
        ),
    error = dict(
            fillpattern = dict(
                fgcolor='red', 
                fillmode='replace', 
                shape="x"),
            line = dict(width=2.0, color='red'),
            mode = "lines",
        ),
    __default__ = dict(
            fillpattern = dict(
                fgcolor='blue', 
                fillmode='replace', 
                shape="x"),
            line = dict(width=2.0, color='blue'),
            mode = "lines",
        ),
)

################################################################################
##                                CHAPTER STYLE                               ##
################################################################################
CHAPTER_STYLES = dict(
    default = dict(
            fillcolor='darkorange',
            opacity=0.7,
            line = dict(width=3.0, color='darkslategray'),
            mode="text",
        ),
    __start__ = dict(
            fillcolor='crimson',
            line = dict(width=3.0, color='darkslategray'),
            mode="text",
        ),
    __end__ = dict(
            fillcolor='crimson',
            line = dict(width=3.0, color='darkslategray'),
            mode="text",
        ),
    __default__ = dict(
            fillcolor='darkorange',
            opacity=0.7,
            line = dict(width=3.0, color='darkslategray'),
            mode="text",
        ),
)


################################################################################
##                                  EDGE STYLE                                ##
################################################################################
EDGE_STYLES = dict(
    default = dict(
            fillcolor='dimgray',
            line = dict(width=1.0, color='black'),
            mode = "lines",
        ),
    __default__ = dict(
            fillcolor='blue',
            line = dict(width=1.0, color='black'),
            mode = "lines",
        ),
)