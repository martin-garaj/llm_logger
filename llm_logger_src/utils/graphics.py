from plotly import graph_objects as go
from typing import Dict, Any
import numpy as np
from shapely.geometry import LineString


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                              _get_node_trace                               ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _get_node_trace(x:float, y:float, width:float, height:float, 
                    style:Dict[str, Any],
                    ) -> go.Scatter:

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


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                              _get_edge_trace                               ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _get_edge_trace(x_start:float, y_start:float, x_end:float, y_end:float, 
                    width:float, style:Dict[str, Any], raise_error:bool=True,
                    ) -> go.Scatter:
    
    # determine geometry
    #   straight - no knees
    #   perpendicular - knees at 90 [deg] angle
    #   skew - knees at 30 [deg] angle 
    
    # sanity check
    if (x_start == x_end) and (y_start == y_end) and raise_error:
        print(f"x_start = {x_start:.3f}")
        print(f"y_start = {y_start:.3f}")
        print(f"x_end   = {x_end:.3f}")
        print(f"y_end   = {y_end:.3f}")
        raise ValueError(
            f"edge starts and ends at the same point "\
            f"start=[{x_start:.3f}, {y_start:.3f}], "\
            f"end=[{x_end:.3f}, {y_end:.3f}]")
    
    # decide geometry
    geometry = "straight"
    if y_start == y_end:
        geometry = "straight"
    elif np.abs(y_start-y_end) <= np.abs(x_start-x_end):
        geometry = "perpendicular"
    elif np.abs(y_start-y_end) > np.abs(x_start-x_end):
        geometry = "skew_30deg"

    # get line 
    if geometry == "straight":
        points = [(x_start, y_start), 
                    (x_end, y_end)]
    elif geometry == "perpendicular":
        points = [(x_start, y_start), 
                    (x_start, (y_start+y_end)/2), 
                    (x_end  , (y_start+y_end)/2),
                    (x_end  , y_end)]
    elif geometry == "skew_30deg":
        skew_length = np.abs(x_start-x_end) / np.cos(np.pi/12)
        # prevent zig-zag shape in case the y_start is after the y_end 
        # (not before as one could expect)
        if y_start < y_end:
            knee_y_0 = (y_start+y_end)/2-(skew_length/2)
            knee_y_1 = (y_start+y_end)/2+(skew_length/2)
        else:
            knee_y_0 = (y_start+y_end)/2+(skew_length/2)
            knee_y_1 = (y_start+y_end)/2-(skew_length/2)
        points = [(x_start, y_start), 
                    (x_start, knee_y_0), 
                    (x_end  , knee_y_1),
                    (x_end  , y_end)]
    else:
        raise NotImplementedError(\
            f"geometry='{geometry}' is not implemented!")
    line = LineString(points)
    
    # get polygon (by buffering the line)
    buffered_line = line.buffer(
            distance=width, 
            quad_segs=0, 
            cap_style="round", #"flat", 
            join_style="mitre",
        )
    
    # get trace
    x, y = list(zip(*buffered_line.exterior.coords))
    trace = go.Scatter(
        x = x,
        y = y,
        fill = "toself",
        **style,
    )
    
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                             _get_chapter_trace                             ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _get_chapter_trace(x:float, y:float, width:float, height:float,
                    style:Dict[str, Any],
                    ) -> go.Scatter:
    
    top = y + (height/2)
    middle = y
    bottom = y - (height/2)
    left = x - (width/2)
    right = x + (width/2)
    skew_length = (height/2)

    x = [  left,   left+skew_length, right-skew_length,  right, 
         right-skew_length, left+skew_length,   left]
    y = [middle,                top,               top, middle,            
                    bottom,           bottom, middle]
    
    trace = go.Scatter(
        x = x,
        y = y,
        fill = "toself",
        **style,
    )
    
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                               _set_node_text                               ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _set_node_text(trace:go.Scatter, 
                   trace_index:int,
                    data:dict=None, 
                    metadata:dict=None, 
                    excerpt_len:int=50,
                    ) -> go.Scatter:
    
    
    content = "" if data is None else str(data.get("content", ""))
    time = "" if metadata is None else str(metadata.get("time", "time unknown"))
    column = "" if metadata is None else str(metadata.get("column", "no label"))
    
    # appears as label
    # trace["text"] = [str(column).replace('\n', '<br />')]
    
    # appears on hover
    if len(content) > excerpt_len:
        excerpt = content[0:excerpt_len-4] + " ..."
    else:
        excerpt = content
        
    trace['hoverinfo'] = "name" # text, name, none (no hover)
    # trace["name"] = \
    #       time + '<br />' \
    #     + column + '<br />' \
    #     + '<br /> ======= CONTENT EXCERPT ======= <br />' \
    #     + excerpt.replace('\n', '<br />')
    
    trace["name"] = excerpt.replace('\n', '<br />')   
    
    # appears in the display window
    trace["customdata"] = [
        dict(trace_index=trace_index, # pointer to this within figure
             content_lines=content.split('\n'),
        ),
    ]
    
    return trace

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                              _set_chapter_text                             ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _set_chapter_text(trace:go.Scatter, 
                    trace_index:int,
                    data:dict=None, 
                    metadata:dict=None, 
                    excerpt_len:int=50,
                    ) -> go.Scatter:
    
    trace['hoverinfo'] = "none" # text, name, none (no hover)
    # appears as label
    # trace["text"] = [str(data["title"]).replace('\n', '<br />')]

    trace["customdata"] = [
        dict(trace_index=trace_index, # pointer to this within figure
        ),
    ]
    
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                               _set_edge_text                               ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _set_edge_text(trace:go.Scatter, 
                    trace_index:int,
                    data:dict=None, 
                    metadata:dict=None, 
                    excerpt_len:int=50,
                    ) -> go.Scatter:
    

    trace['hoverinfo'] = "none" # text, name, none (no hover)
    trace["customdata"] = [
        dict(trace_index=trace_index, # pointer to this within figure
        ),
    ]
    
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                               _set_edge_text                               ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _get_annotation(x:float, y:float, text:str, style:dict):
    
    # not available to user
    style["captureevents"] = False
    style["showarrow"] = False
    
    annotation = dict(
        x=x,
        y=y,
        text=text,
        # font=dict(
        #     family="Courier New, monospace",
        #     size=16,
        #     color="#ffffff"
        #     ),
        # align="center",
        # captureevents = False,
        # showarrow  = False,
        **style,
    )

    return annotation
################################################################################
##                                    TESTS                                   ##
################################################################################
if __name__ == "__main__":
    
    # define parameters
    node_width = 0.3
    node_height = 0.1
    edge_width = 0.02
    
    # define nodes
    node_0_center = (1.0, 2.0)
    node_1_center = (1.0, 6.0)
    node_2_center = (5.0, 3.0)
    node_3_center = (4.0, -3.0)
    
    # plot
    fig = go.Figure()
    node_centers = [node_0_center, node_1_center, node_2_center, node_3_center]
    
    # plot edges
    for node_center in node_centers:
        try:
            fig.add_trace(
                _get_edge_trace(
                    x_start = node_0_center[0],
                    y_start = node_0_center[1],
                    x_end = node_center[0], 
                    y_end = node_center[1], 
                    width=edge_width, 
                    style = dict(
                        line = dict(width=3.0, color='blue'),
                        mode = "lines",
                    ),
                )
            )
        except ValueError:
            print(f"caught exception")
            continue
    
    # plot nodes
    for node_center in node_centers:
        fig.add_trace(
            _get_node_trace(
                x = node_center[0],
                y = node_center[1],
                width = node_width,
                height = node_height,
                style = dict(
                    line = dict(width=3.0, color='red'),
                    mode = "lines",
                ),
            )
        )

    # fig.update_xaxes(showgrid=False)
    fig.update_layout(
        yaxis = dict(autorange="reversed"),
        xaxis_range=[-10,10],
        yaxis_range=[-10,10],
        yaxis_scaleanchor="x",
    )
    fig.show()
    