from dash import Input, Output, State
from dash.exceptions import PreventUpdate

try:
    from llm_logger_src.utils.ids import _NODE, _CHAPTER, _EDGE
except ImportError:
    raise ImportError("unable to import from 'ids'")

def register_fig_highlight_traces(app):
    @app.callback(
        Output('fig-graph', 'figure', allow_duplicate=True),
        [Input('fig-graph', 'clickData'),
         State('fig-graph', 'figure'),
         State('fig-related-traces', 'data'),
         State('fig-node-styles', 'data'),
         State('fig-chapter-styles', 'data'),
         State('fig-edge-styles', 'data'),
        ],
        prevent_initial_call=True,
    )
    def fig_highlight_traces(clickData, figure, relatedTraces, nodeStyles, chapterStyles, edgeStyles):
        if not clickData or not figure or not relatedTraces:
            raise PreventUpdate

        try:
            trace_index = clickData['points'][0]['customdata'][0]["metadata"]["trace_index"]
            related_indices = relatedTraces[str(trace_index)]
            print(f'fig_highlight_traces() -> index = {trace_index} -> related_indices={related_indices}')
        except (KeyError, IndexError, TypeError):
            raise PreventUpdate

        # fast-lookup for trace styles
        trace_type_to_styles = {
            f"{_NODE}":nodeStyles,
            f"{_CHAPTER}":chapterStyles,
            f"{_EDGE}":edgeStyles,
        }

        
        # Reset styles for all traces to their default
        for trace in figure['data']:
            # TODO: Continue here once the datastruct is updated.
            trace_type = trace["customdata"][0]["metadata"]["trace_type"]
            trace_style = trace["customdata"][0]["metadata"]["trace_style"]
            print(f'fig_highlight_traces() -> index = {trace["customdata"][0]["metadata"]["trace_index"]} -> trace_style={trace_style}')
            trace.update(trace_type_to_styles[trace_type][trace_style])

        # Highlight the clicked trace and related traces
        for index in [trace_index] + related_indices:
            # get trace
            trace = figure['data'][int(index)]
            
            trace_type = trace["customdata"][0]["metadata"]["trace_type"]
            trace_style = trace["customdata"][0]["metadata"]["trace_style"]
            trace_style = trace_style+"_selected"
            
            print(f"fig_highlight_traces() -> index = {index} -> trace_style={trace_style}")
            trace.update(trace_type_to_styles[trace_type][trace_style])
            
        return figure
