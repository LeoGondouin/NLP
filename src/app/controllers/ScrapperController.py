from dash import Input, Output, State,html
from server import app
from views.scrapper.scrapper import scrapper_screen
import time
import dash_core_components as dcc
import threading
import requests
import json

@app.callback(
    Output('screen-menu','children',allow_duplicate=True),
    Input('menu-scrapper','n_clicks'),
)
def display(n_clicks):
    if n_clicks is not None:
        return scrapper_screen
    
@app.callback(
    Output('span-preview','children',allow_duplicate=True),
    Input('txt-keyword','value'),
    Input('cb-nbdocs','value'),
    Input('cb-website','value'),
)    
def displayReminder(keyword,nbDocs,websites):
    if keyword is not None and nbDocs is not None and websites is not None:
        return [
            "You will start a Web Scrap on the following websites : ",
            html.Span(children=', '.join([item.capitalize() for item in websites]), style={"font-weight": "bold"}),
            " which will return approximately ",
            html.Span(children=int(nbDocs) * len(websites), style={"font-weight": "bold"}),
            " documents on the keyword : ",
            html.Span(children=keyword, style={"font-weight": "bold"})
        ]

def simulate_delay(callback):
    time.sleep(2)
    callback()

@app.callback(
    Output('span-preview', 'children',allow_duplicate=True),
    State('txt-keyword','value'),
    State('cb-nbdocs','value'),
    State('cb-website','value'),
    Input('btn-scrap','n_clicks'),
)        
def scrapOutput(keywords, nbDocs, websites, n_clicks):
    if n_clicks is not None:
        url = 'http://scraping_api:5001/scrap/offers'

        data = {
            'keywords': keywords,
            'nb_docs': nbDocs,
            'websites': websites,
        }

        headers = {'Content-Type': 'application/json'}  # Set content type to JSON

        response = requests.post(url, json=data, headers=headers)  # Send data as JSON in the request body
        corpus = list()

        isScrapped = True
        isInserted = True

        # Check the response
        if response.status_code == 200:
            print('Scrappage réussi')
            corpus = response.json()
        else:
            print(f'POST request failed with status code: {response.status_code}')
            print('Response:', response.text)
            isScrapped = False

        url = 'http://db_api:5002/insert/offers'

        response = requests.post(url, json=json.loads(corpus),headers=headers)

        if response.status_code == 200:
            print('Insertion en base de données réussie')
        else:
            print(f'POST request failed with status code: {response.status_code}')
            print('Response:', response.text)
            isInserted = False

        strResponse = ""
        if not(isScrapped):
            strResponse = "ERROR : Job scrapping failed"
        elif not(isInserted):
            strResponse = "ERROR : Corpus saving failed"
        else:
            strResponse = "SUCCESS : Corpus saved !"
            
        return strResponse
        
        


