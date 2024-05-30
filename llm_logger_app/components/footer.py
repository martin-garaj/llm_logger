from dash import html

def footer() -> html.Div:
    footer = html.Div(
        id="app-footer",
        className="footer",
        children=[
            html.Div(className="flex_1"),
            # html.Div("Developed by "),
            html.Div(
                className="footer-logo-container",
                children=html.A(
                    href='https://www.alphaprompt.ai',
                    target='_blank',
                    children=html.Img(
                            id='footer-logo', 
                            className='footer-logo',
                            src='/assets/logo_hor_v1.svg', 
                            )
                )  
                ),
        ]
    )
      
    
    
    return footer