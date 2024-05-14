
from plotly import graph_objects as go
import copy
from typing import Any

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

    from ids import _NODE, _CHAPTER, _EDGE
else:

    try:
        from .ids import _NODE, _CHAPTER, _EDGE
    except ImportError:
        from llm_logger_src.utils.ids import _NODE, _CHAPTER, _EDGE



_DATASTRUCT = {
    "metadata":{
        "trace_type":None, # _NODE, _CHAPTER, _EDGE
        "trace_style":None, # defined in styles.py
        "trace_index":None, # defined within llm_parser
    },
    "data":{
        "title":"<title>",
        "content":None,
    },
}


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                              init_customdata                               ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def init_customdata(
        trace:go.Scatter, 
        trace_index:int, 
        trace_type:str=None,
        trace_style:str=None,
        title:str=None,
        content:Any=None,
        ):
    
    # sanity check
    _check_trace_index(trace_index)

    # initialize structure
    trace["customdata"] = list([copy.deepcopy(_DATASTRUCT)])
    trace["customdata"][0]["metadata"]["trace_index"] = trace_index
    
    
    trace = update_metadata(
        trace=trace, 
        trace_type=trace_type,
        trace_style=trace_style,
    )
    
    trace = update_data(
        trace=trace, 
        title=title,
        content=content,
    )
    
    return trace


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                              print_customdata                              ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def print_customdata(trace:go.Scatter, excerpt_len:int=50):
    content_excerpt = str(get_trace_content(trace))[0:excerpt_len]
    content_excerpt = content_excerpt.replace("\n", "\n"+(" "*29))
    string = \
        f'trace ({type(trace)}):\n'\
        f'   ├── metadata :\n'\
        f'   |  ├── trace_type      : {get_trace_type(trace)}\n'\
        f'   |  ├── trace_style     : {get_trace_style(trace)}\n'\
        f'   |  └── trace_index     : {get_trace_index(trace)}\n'\
        f'   └── data : \n'\
        f'      ├── title           : {get_trace_title(trace)}\n'\
        f'      └── content         : "{content_excerpt}"'
    print(string)
    return string


################################################################################
##                                   SETTERS                                  ##
################################################################################
def update_metadata(
        trace:go.Scatter, 
        trace_type:str=None,
        trace_style:str=None,
    ):
    try:
        if not isinstance(trace_type, type(None)):
            trace["customdata"][0]["metadata"]["trace_type"] = trace_type
        if not isinstance(trace_style, type(None)):
            trace["customdata"][0]["metadata"]["trace_style"] = trace_style
    except KeyError:
        raise RuntimeError(f"Trace not initialized!")
    return trace

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                                 update_data                                ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def update_data(trace:go.Scatter, title:str=None, content:Any=None):
    try:
        if not isinstance(title, type(None)):
            trace["customdata"][0]["data"]["title"] = title
        if not isinstance(content, type(None)):
            trace["customdata"][0]["data"]["content"] = content
    except KeyError:
        raise RuntimeError(f"Trace not initialized!")
    return trace


################################################################################
##                                   GETTERS                                  ##
################################################################################
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                                  get_type                                  ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def get_trace_type(trace:go.Scatter):
    try:
        return trace["customdata"][0]["metadata"]["trace_type"]
    except KeyError:
        raise RuntimeError(f"Trace not initialized!")
    
    
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                                 get_style                                  ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def get_trace_style(trace:go.Scatter):
    try:
        return trace["customdata"][0]["metadata"]["trace_style"]
    except KeyError:
        raise RuntimeError(f"Trace not initialized!")


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                              get_trace_index                               ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def get_trace_index(trace:go.Scatter):
    try:
        return trace["customdata"][0]["metadata"]["trace_index"]
    except KeyError:
        raise RuntimeError(f"Trace not initialized!")


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                                get_content                                 ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def get_trace_title(trace:go.Scatter):
    try:
        return trace["customdata"][0]["data"]["title"]
    except KeyError:
        raise RuntimeError(f"Trace not initialized!")
    

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                                get_content                                 ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def get_trace_content(trace:go.Scatter):
    try:
        return trace["customdata"][0]["data"]["content"]
    except KeyError:
        raise RuntimeError(f"Trace not initialized!")


################################################################################
##                                SANITY CHECKS                               ##
################################################################################

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##                                _check_index                                ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
def _check_trace_index(trace_index):
    # default value
    if isinstance(trace_index, type(None)):
        return
    if not isinstance(trace_index, int) or trace_index < 0:
        raise RuntimeError(
            f"trace_index='{trace_index}', type(index)={type(trace_index)} "
            f"but only trace_index >= 0 and {type(int)} is valid!")


################################################################################
##                                    TEST                                    ##
################################################################################
if __name__ == "__main__":
    
    trace = go.Scatter(
        x=[1, 2], 
        y=[2, 3], 
        mode="lines", 
        line=dict(color="blue", width=3),
    )

    
    trace = init_customdata(trace, trace_index = 0)
    
    # trace = init_customdata(
    #     trace = trace, 
    #     trace_type = _NODE,
    #     trace_style = "__default__",
    #     trace_index = 0, 
    #     content=None,
    #     )
    
    trace = update_metadata(trace, trace_type = _NODE, trace_style="__default__")
    
    try:
        trace = update_metadata(trace, trace_type = _NODE, trace_style="__default__")
    except TypeError:
        print(f"PASS:   update_metadata(trace, state=8) -> RuntimeError")
        

    trace = update_data(trace, title="TITLE", content=['kkk'])

    print_customdata(trace)