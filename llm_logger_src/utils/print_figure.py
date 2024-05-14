from plotly import graph_objects as go
import time
import numpy as np


_SELECTED = 1
_UNSELECTED = 0

some_long_list_to_check = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]


def change_figure(figure):
    _start_time = time.time()
    OK = 0
    for trace in figure.data:
        try:
            if trace['customdata'][0]['metadata']['id'] in some_long_list_to_check:
                if trace['customdata'][0]['metadata']['id'] + 1 in some_long_list_to_check:
                    if trace['customdata'][0]['metadata']['state'] == _SELECTED:
                        trace['customdata'][0]['metadata']['state'] = _UNSELECTED
                    else:
                        trace['customdata'][0]['metadata']['state'] == _SELECTED
                    OK = OK + 1
        except Exception:
            continue
    _elapsed_time = time.time() - _start_time
    return _elapsed_time, OK


# def print_figure(figure:go.Figure):
    
#     print(f"============================= FIGURE =============================")
#     for trace in figure.data:
#         try:
#             if trace['customdata'][0]['metadata']['state'] == _SELECTED:
#                 trace['customdata'][0]['metadata']['state'] = _UNSELECTED
#             else:
#                 trace['customdata'][0]['metadata']['state'] == _SELECTED
#         except Exception:
#             continue

#     print(f"=========================== FIGURE END ===========================")
#     return 



K = 500

if __name__ == "__main__":
    
    
    ################################## TRACES ##################################
    traces = list()
    for k in range(K):
        if K % 2 == 0:
            trace = go.Scatter(
                x=[k,k-2],
                y=[k,k+2],
                line=dict(color="blue"),
                customdata=[
                    dict(
                        data=[f"Some text representing data {k}"],
                        metadata=dict(
                            id=np.random.randint(0, 5),
                            related= list(range(k)),
                            state=_SELECTED,
                        )
                    )
                ]
            )
        else:
            trace = go.Scatter(
                x=[k,k-2],
                y=[k,k+2],
                line=dict(color="red"),
            )
        traces.append(trace)
    
    
    ################################## FIGURE ##################################
    figure = go.Figure(data=traces, layout=go.Layout(xaxis=dict(range=[0 ,3])))
    
    
    ################################### OTHER ##################################
    figure.add_vrect(
        x0=0.5,
        x1=1.5,
        fillcolor='gainsboro',
        opacity=0.9,
        line_width=0,
        layer="below",
    )
    
    for a in range(3):
        figure.add_annotation(
            dict(x=a, y=a, text=f"annotation = {a}")
        )
    
    ################################ PRINT / SHOW ##############################
    elapsed_time, OK = change_figure(figure)
    
    print(f"Change took {elapsed_time:.3f} [s] (OK={OK})")
    
    ################################ PRINT / SHOW ##############################
    # print_figure(figure)
    
    # print(figure)
    # figure.show()