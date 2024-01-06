from dash import Input, Output, State,html
from server import app
from views.scrapper.scrapper import scrapper_screen
import time
import dash_core_components as dcc
import threading
from api.scrapper.functions import scrapCorpus

@app.callback(
    Output('screen-menu','children',allow_duplicate=True),
    Input('menu-scrapper','n_clicks'),
)
def display(n_clicks):
    if n_clicks is not None:
        return scrapper_screen
    
@app.callback(
    Output('span-preview','children'),
    Input('txt-keyword','value'),
    Input('cb-nbdocs','value'),
    Input('cb-website','value'),
)    
def display_reminder(keyword,nbDocs,websites):
    if keyword is not None and nbDocs is not None and websites is not None:
        return [
            "Vous allez lancer un Web Scrapping sur les sites : ",
            html.Span(children=', '.join(websites), style={"font-weight": "bold"}),
            " qui va retourner environ : ",
            html.Span(children=int(nbDocs) * len(websites), style={"font-weight": "bold"}),
            " documents sur le thème : ",
            html.Span(children=keyword, style={"font-weight": "bold"})
        ]

def simulate_delay(callback):
    time.sleep(2)
    callback()

@app.callback(
    Output('loading-placeholder', 'children'),
    State('txt-keyword','value'),
    State('cb-nbdocs','value'),
    State('cb-website','value'),
    Input('btn-scrap','n_clicks'),
)        
def scrapOutput(keywords,nbDocs,websites,n_clicks):
    if n_clicks is not None:
        corpus = scrapCorpus(websites,keywords,nbDocs)
        print(corpus)

