from dash import Input, Output, State
from dash import dcc
from dash import html
from server import app
from views.dashboard.topic_analysis import topic_analysis
from .functions.topicAnalysisHelper import generateScatterClusters
import pandas as pd
import requests
import json

@app.callback(
    Output('screen-menu','children',allow_duplicate = True),
    Input('menu-topic-analysis','n_clicks')
)
def display(n_clicks):
    if n_clicks:
        url = "http://db_api:5002/get/offers?criterias="

        fullUrl = url

        response = requests.get(fullUrl)

        if response.status_code == 200:
            global cube
            cube = pd.DataFrame.from_records(json.loads(response.json()))
            if cube.shape[0]>0:
                cb_nbClusters = dcc.Dropdown(id="cb-cluster",options=[{'label': str(i), 'value': i} for i in range(2, 11)],value=3)
                cb_subject = dcc.Dropdown(id="cb-subject",options=[{'label':column.capitalize(),'value': column} for column in cube.drop(columns=["longitude","latitude"]).columns],value="website")
                btn_ReCompute = html.Button(id="btn-recompute",children="Re-Compute")
                scatter_cluster = dcc.Graph(id="scatter-clusters",figure=generateScatterClusters(cube,"website",3))
                return [topic_analysis]+[cb_nbClusters,cb_subject,btn_ReCompute,scatter_cluster]

@app.callback(
    Output('scatter-clusters','figure'),
    Input('btn-recompute','n_clicks'),
    State('cb-cluster','value'),
    State('cb-subject','value')
)
def reCompute(n_clicks,nbClusters,subject):
    global cube
    if n_clicks:
        return generateScatterClusters(cube,subject,nbClusters)
    else:
        return generateScatterClusters(cube,"website",3)
    
