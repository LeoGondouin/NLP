from dash import Input, Output, State
from dash import dcc
from dash import html
from server import app
from views.dashboard.descriptive_statistics import statistics
from views.dashboard.corpus_analysis import corpus_analysis
import requests 
from dash_table import DataTable
import pandas as pd
import plotly.express as px
import json

cube = None

@app.callback(
    Output('screen-menu','children',allow_duplicate = True),
    Input('menu-dashboard','n_clicks')
)
def display(n_clicks):
    if n_clicks is not None:
        response = requests.get("http://db_api:5002/get/offers")
        if response.status_code == 200:
            global cube
            cube = pd.DataFrame.from_records(json.loads(response.json()))
            contract_type_prop = cube['contract_type'].value_counts()
            website_prop = cube['website'].value_counts()
            company_prop = cube['company'].value_counts()
            descriptives_stats = [
                    html.Span(children=[
                                    html.Label(
                                        children=str(len(company_prop.index)),
                                        style={"font-weight":"bold"}
                                    ),
                                    " distinct count of companies"
                                ]
                            ,style={"font-size":"22px"}
                            ),
                    html.Span("Average number of words by offer",style={"padding-left":"5px"}),
                    html.Div(children=[
                                html.Div([
                                    dcc.Graph(
                                        id="pie-contract_type",
                                        figure=px.pie(
                                            names=contract_type_prop.index, 
                                            values=contract_type_prop.values, 
                                            title='Distribution of Contract types'
                                        ),
                                    ),
                                    dcc.Graph(
                                        id="bar-website",
                                        figure=px.bar(
                                            x=website_prop.index, 
                                            y=website_prop.values, 
                                            title='Distribution of offers by websites',
                                            labels={'x': 'Websites', 'y': 'Counts'}
                                        )
                                    )
                                ]),
                                html.Div([
                                    dcc.Graph(
                                        id="bar-company",
                                        figure=px.bar(
                                            x=company_prop.index, 
                                            y=company_prop.values, 
                                            title='Distribution of offers by companies',
                                            labels={'x': 'Companies', 'y': 'Counts'}
                                        )
                                    )    
                                ])   
                        ]
                    ,style={"display":"flex"})
            ]
        return [statistics]+descriptives_stats