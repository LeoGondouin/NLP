import dash_html_components as html
import dash_core_components as dcc
import numpy as np

website_options = [
    {'label': 'Apec', 'value': 'apec'},
    {'label': 'Emploi territorial', 'value': 'emploi-territorial'},
    {'label': 'HelloWork', 'value': 'hellowork'},
    {'label': 'Pôle Emploi', 'value': 'pole-emploi'},
    {'label': 'Welcome to the Jungle', 'value': 'welcometothejungle'},
]

scrapper_screen = html.Div(
    [
        html.H1("Job scrapper"),
        html.Label("Select Website(s)", style={'margin-bottom': '5px'}),
        dcc.Dropdown(id="cb-website", options=website_options, multi=True, style={'width': '100%', 'margin-bottom': '15px'}),
        
        html.Label("Enter Search Keywords", style={'margin-bottom': '5px'}),
        dcc.Input(id="txt-keyword", type="text", placeholder="Type in search keywords", style={'width': '100%', 'margin-bottom': '15px', 'text-align': 'center', 'border': '1px solid #ddd', 'border-radius': '5px', 'padding': '8px'}),
        
        html.Br(),
        
        html.Label("Select Number of Documents", style={'margin-bottom': '5px'}),
        dcc.Dropdown(id="cb-nbdocs", options=[{'label': i, 'value': i} for i in np.arange(5, 55, 5)],
                     style={'width': '100%', 'margin-bottom': '15px'}),
        
        html.Div([
            html.Label("Preview: "),
            html.Span(id="span-preview", style={'margin-right': '10px'}),
        ], style={'margin-bottom': '15px'}),
        
        html.Button('Scrap Data', id='btn-scrap', style={'width': '100%'}),
    ],
    style={'height': '100vh', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center', 'max-width': '400px', 'margin': 'auto', 'border': '1px solid #ddd', 'border-radius': '10px', 'padding': '20px'}
)
