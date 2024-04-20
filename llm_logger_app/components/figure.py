from dash import html, dcc

def figure() -> html.Div:
    chapters = list()
    chapters.append(html.Div(id="fig-chapter-start", 
                             children=[f"α"],  
                             className="fig-chapter-selected"))
    chapters.append(html.Div(id="fig-chapter-end", 
                             children=[f"ω"],  
                             className="fig-chapter"))

    figure_div = html.Div(
                id="fig-content",
                className="fig-content",
                children=[ 
                    html.Div(id="fig-blank",  
                             className="fig-blank"),
                    html.Div(id="fig-title",  
                             className="fig-title", 
                             children=["Chapter title"]),
                    html.Div(id="fig-index",  
                             className="fig-index hide-scrollbar", 
                             children=chapters),
                    html.Div(id="fig-plotly", 
                             className="fig-plotly", 
                             children=[dcc.Graph(id="plotly-figure", className="fig-plotly")]),
                        ],
                )
    
    return figure_div





