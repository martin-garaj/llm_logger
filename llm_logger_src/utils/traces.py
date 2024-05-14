from plotly import graph_objects as go
from typing import Dict, Any
import numpy as np
from shapely.geometry import LineString

if __name__ == "__main__":
    import sys
    import os
    import pathlib as pl
    file_path = pl.Path(__file__).parent
    try:
        sys.path.index(file_path)
    except ValueError:
        sys.path.append(file_path)
    project_root_in_sys = sys.path[sys.path.index(file_path)]
    print(f"TESTING: add '{project_root_in_sys}' to PYTHONPATH")
    
    from customdata import init_customdata, \
        update_metadata, update_data, get_trace_index, get_trace_type, \
        get_trace_style, get_trace_content 
    from ids import _NODE, _CHAPTER, _EDGE
    
else:
    try:
        from .customdata import init_customdata, \
        update_metadata, update_data, get_trace_index, get_trace_type, \
        get_trace_style, get_trace_content 
        from .ids import _NODE, _CHAPTER, _EDGE
    except ImportError:
        from llm_logger_src.utils.customdata import init_customdata, \
        update_metadata, update_data, get_trace_index, get_trace_type, \
        get_trace_style, get_trace_content 
        from llm_logger_src.utils.ids import _NODE, _CHAPTER, _EDGE


################################################################################
##                                  GRAPHICS                                  ##
################################################################################
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                              _get_node_trace                               ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _get_node_trace(
            x:float, 
            y:float, 
            width:float, 
            height:float, 
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
def _get_edge_trace(
            x_start:float, 
            y_start:float, 
            x_end:float, 
            y_end:float, 
            width:float, 
            style:Dict[str, Any], 
            raise_error:bool=True,
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
def _get_chapter_trace(
            x:float, 
            y:float, 
            width:float, 
            height:float,
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



################################################################################
##                                 DATASTRUCT                                 ##
################################################################################
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                            _set_node_datastruct                            ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _set_node_datastruct(
            trace:go.Scatter, 
            trace_index:int,
            trace_style:str=None,
            data:dict=None, 
            excerpt_len:int=50,
        ) -> go.Scatter:
    
    if not isinstance(trace_index, int) or trace_index < 0:
        raise ValueError(
            f"trace_index={trace_index} (type={type(trace_index)}), "\
            f"but only type={type(trace_index)} and trace_index>=0 is valid!")
    
    content = "" if data is None else str(data.get("content", ""))
    # time = "" if metadata is None else str(metadata.get("time", "time unknown"))
    # column = "" if metadata is None else str(metadata.get("column", "no label"))

    trace['hoverinfo'] = "name" # text, name, none (no hover)
    # appears on hover
    if len(content) > excerpt_len:
        excerpt = content[0:excerpt_len] + " ..."
    else:
        excerpt = content
    trace["name"] = excerpt.replace('\n', '<br />')
    
    trace = init_customdata(
        trace=trace, 
        trace_index=trace_index,
        trace_type=_NODE,
        trace_style=trace_style,
        content=content,
        )
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                           _set_chapter_datastruct                          ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _set_chapter_datastruct(
            trace:go.Scatter, 
            trace_index:int,
            trace_style:str=None,
            data:dict=None, 
        ) -> go.Scatter:
    
    if not isinstance(trace_index, int) or trace_index < 0:
        raise ValueError(
            f"trace_index={trace_index} (type={type(trace_index)}), "\
            f"but only type={type(trace_index)} and trace_index>=0 is valid!")  
    
    trace['hoverinfo'] = "none" # text, name, none (no hover)

    trace = init_customdata(
        trace, 
        trace_index=trace_index,
        trace_type=_CHAPTER,
        trace_style=trace_style,
        title=data.get("title", None),
        content=data.get("content", None),
        )
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                            _set_edge_datastruct                            ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _set_edge_datastruct(
            trace:go.Scatter, 
            trace_index:int,
            trace_style:str=None,
            data:dict=None, 
            excerpt_len:int=50,
        ) -> go.Scatter:
    
    if not isinstance(trace_index, int) or trace_index < 0:
        raise ValueError(
            f"trace_index={trace_index} (type={type(trace_index)}), "\
            f"but only type={type(trace_index)} and trace_index>=0 is valid!") 
    
    content = "" if data is None else str(data.get("content", ""))
    # time = "" if metadata is None else str(metadata.get("time", "time unknown"))
    # column = "" if metadata is None else str(metadata.get("column", "no label"))

    trace['hoverinfo'] = "name" # text, name, none (no hover)
    # appears on hover
    if len(content) > excerpt_len:
        excerpt = content[0:excerpt_len] + " ..."
    else:
        excerpt = content
    trace["name"] = excerpt.replace('\n', '<br />')
    
    trace = init_customdata(
        trace, 
        trace_index=trace_index,
        trace_type=_EDGE,
        trace_style=trace_style,
        content=content,
        )
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                             _set_node_metadata                             ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _set_node_metadata(
            trace:go.Scatter, 
            trace_style:str=None,
        ) -> go.Scatter:
    trace = update_metadata(
        trace=trace,
        trace_style=trace_style,
    )
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                             _set_edge_metadata                             ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _set_edge_metadata(
            trace:go.Scatter, 
            trace_style:str=None,
        ) -> go.Scatter:
    trace = update_metadata(
        trace=trace,
        trace_style=trace_style,
    )
    return trace


################################################################################
##                                 ANNOTATION                                 ##
################################################################################
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                               _get_annotation                              ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _get_annotation(
            x:float, 
            y:float, 
            text:str, 
            style:dict,
        ):
    
    # not available to user
    style["captureevents"] = False
    style["showarrow"] = False
    
    annotation = dict(
        x=x,
        y=y,
        text=text,
        **style,
    )

    return annotation


################################################################################
##                                    TESTS                                   ##
################################################################################
if __name__ == "__main__":
    import sys
    import os
    import pathlib as pl
    project_root = pl.Path(os.getcwd()).absolute()
    try:
        sys.path.index(project_root)
    except ValueError:
        sys.path.append(project_root)
    project_root_in_sys = sys.path[sys.path.index(project_root)]
    print(f"TESTING: add '{project_root_in_sys}' to PYTHONPATH")


    # define parameters
    node_width = 2
    node_height = 1
    edge_width = 0.2
    
    # define nodes
    node_0_center = (1.0, 2.0)
    node_1_center = (1.0, 6.0)
    node_2_center = (5.0, 3.0)
    node_3_center = (4.0, -3.0)
    
    # plot
    fig = go.Figure()
    node_centers = [node_0_center, node_1_center, node_2_center, node_3_center]
    
    trace_index_counter = 0
    
    # plot edges
    for node_center in node_centers:
        try:
            trace = _get_edge_trace(
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
            trace = _set_edge_datastruct(
                    trace=trace, 
                    trace_index=trace_index_counter,
                    trace_style="__default__",
                    data=dict(content=["Some edge data."]), 
                    excerpt_len=50,
                )
            fig.add_trace(trace)
            trace_index_counter = trace_index_counter + 1
        except ValueError:
            print(
                f"caught exception for node_center = {node_center}, "\
                f"circular edges are not allowed!")
            continue
    
    # plot nodes
    for node_center in node_centers:
        trace = _get_node_trace(
                x = node_center[0],
                y = node_center[1],
                width = node_width,
                height = node_height,
                style = dict(
                    line = dict(width=3.0, color='red'),
                    mode = "lines",
                ),
            )
        trace = _set_node_datastruct(
                    trace=trace, 
                    trace_index=trace_index_counter,
                    trace_style="__default__",
                    data=dict(content=["Some data."]), 
                    excerpt_len=50,
                    )
        fig.add_trace(trace)
        trace_index_counter = trace_index_counter + 1

    # fig.update_xaxes(showgrid=False)
    fig.update_layout(
        yaxis = dict(autorange="reversed"),
        xaxis_range=[-10,10],
        yaxis_range=[-10,10],
        yaxis_scaleanchor="x",
    )
    fig.show()
    