from dash import Input, Output, State
import json 

def register_store_report(app):
    @app.callback(
        Output('button-debug', 'n_clicks'),
        [Input('button-debug', 'n_clicks'),
        State('fig-chapter-locations', 'data'),
        State('fig-scroll-data', 'data'),
        State('fig-graph-aspect-ratio', 'children'),
        ],
        prevent_initial_call=True,
    )
    def store_report(n_clicks, chapter_locations_data, scroll_data, aspect_ratio_data):
        
        print(f"store(id=fig-chapter-locations)")
        print(f"   data type = {type(chapter_locations_data)}")
        print(json.dumps(chapter_locations_data, indent=2))
        
        print(f"store(id=fig-scroll-data)")
        print(f"   data type = {type(scroll_data)}")
        print(json.dumps(scroll_data, indent=2))
        
        print(f"store(id=fig-graph-aspect-ratio)")
        print(f"   data type = {type(aspect_ratio_data)}")
        print(json.dumps(aspect_ratio_data, indent=2))
        
        return n_clicks