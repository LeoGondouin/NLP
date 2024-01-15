from dash import Input, Output, State
from dash import dcc
from dash import html
from server import app
from views.dashboard.text_analysis import text_analysis
import requests 
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
from .functions.textAnalysisHelpers import generateUsedWordEvolution,generateWorldCloud,generateBarTechnologies
from .functions.getFilterQuery import getFilterQuery
import numpy as np

level = 1
prevMonth = None
prevYear = None
cube = None

@app.callback(
    Output('screen-menu','children',allow_duplicate = True),
    Input('menu-text-analysis','n_clicks')
)
def displayTextAnalysis(n_clicks):
    if n_clicks:
        url = "http://db_api:5002/get/offers?criterias="

        fullUrl = url

        response = requests.get(fullUrl)

        if response.status_code == 200:
            global cube
            cube = pd.DataFrame.from_records(json.loads(response.json()))
            if cube.shape[0]>0:
                wordcloud = dcc.Graph(id='wc',figure=generateWorldCloud(cube,30)) 
                lb = html.Br()
                roll_up_most_used = html.Button(id='btn-roll-up',children="Roll up",style={'display':'none'})  
                most_used = dcc.Graph(id="line-word",figure=generateUsedWordEvolution(cube,1,None,None)) 
                topTechs = dcc.Graph(id="bar-top-n-tech",figure=generateBarTechnologies(cube,10))
                filters = html.Div(
                    children = [
                            dcc.Dropdown(id="cb-website",options=[{'label': website.capitalize(), 'value': website} for website in cube["website"].unique()],multi=True),
                            dcc.Dropdown(id="cb-contract-type",options=[{'label': contract_type, 'value': contract_type} for contract_type in cube["contract_type"].unique()],multi=True),
                            dcc.Dropdown(id="cb-company",options=[{'label': company, 'value': company} for company in cube["company"].unique()],multi=True),
                            html.Div(
                                id="div-calendar-hierarchy",
                                children=[
                                    dcc.Dropdown(id="cb-year",options=[{'label': year, 'value': year} for year in sorted(cube["published_year"].unique())],multi=True),
                                    dcc.Dropdown(id="cb-month",options=[{'label': month, 'value': month_int} for month, month_int in cube[["published_month", "published_month_int"]].drop_duplicates().sort_values(by='published_month_int').values],multi=True),
                                    dcc.Dropdown(id="cb-date",options=[{'label': date, 'value': date} for date in sorted(cube["published_date"].unique())],multi=True),
                                ]
                            ),
                            html.Div(
                                id="div-location",
                                children=[
                                    dcc.Dropdown(id="cb-region",options=[{'label': region, 'value': region} for region in sorted(cube["region"].unique())],multi=True),
                                    dcc.Dropdown(id="cb-department",options=[{'label': department, 'value': department} for department in sorted(cube["department"].unique())],multi=True),
                                    dcc.Dropdown(id="cb-city",options=[{'label': city, 'value': city} for city in sorted(cube["city"].unique())],multi=True),
                                ]
                            ),
                            html.Button(id='btn-filter',children='Filter'),
                    ]
                )                
                return [text_analysis]+[filters,html.Div([
                                            dcc.Dropdown(id='cb-top-n-wc',options=np.arange(5,51,5),value=30),
                                            wordcloud,lb,lb,lb,lb,
                                            html.Div([
                                                html.Div([
                                                    dcc.Dropdown(id='cb-top-n-tech',options=np.arange(5,30,5),value=10),
                                                    topTechs
                                                ],style={"width":"50%"}),
                                                roll_up_most_used,most_used
                                                ],style={"display":"flex","margin-left":"50px"}
                                            )]
                                        )]

@app.callback(
    Output('wc','figure',allow_duplicate=True),
    Output('bar-top-n-tech','figure',allow_duplicate=True),
    Output('line-word','figure',allow_duplicate=True),
    Input('btn-filter','n_clicks'),
    State('cb-website','value'),
    State('cb-contract-type','value'),
    State('cb-company','value'),
    State('cb-year','value'),
    State('cb-month','value'),
    State('cb-date','value'),
    State('cb-region','value'),
    State('cb-department','value'),
    State('cb-city','value'),
    State('cb-top-n-wc','value'),
    State('cb-top-n-tech','value'),
)
def filter(n_clicks,websites,contract_types,companies,years,months,date,region,department,city,topNWC,topNTechs):
    global level
    if n_clicks is not None:
        level=1
        prevYear=None
        prevMonth=None

        url = "http://db_api:5002/get/offers?criterias="

        fullUrl = getFilterQuery(url,websites,contract_types,companies,years,months,date,region,department,city)

        response = requests.get(fullUrl)

 
        empty_graphs = html.Label("No data available"),px.bar(
                                    title='No data available',
                                    labels={'y': 'Technology', 'x': 'Frequency'},
                                    orientation="h"
                                ),px.line(
                                    title='No data available',
                                    labels={'y': 'Frequency', 'x': 'Published_year'},
                                    orientation="h"
                                )
        
        if response.status_code == 200:
            cube = pd.DataFrame.from_records(json.loads(response.json()))
            if cube.shape[0]>0:
                wordcloud = generateWorldCloud(cube,topNWC)
                most_used = generateUsedWordEvolution(cube,1,prevYear,prevMonth)
                topTechs = generateBarTechnologies(cube,topNTechs)
                return wordcloud,topTechs,most_used
            else:
                return empty_graphs
            
    if cube.shape[0]>0:
        wordcloud = generateWorldCloud(cube,topNWC)
        most_used = generateUsedWordEvolution(cube,1,prevYear,prevMonth)
        topTechs = generateBarTechnologies(cube,topNTechs)
        return wordcloud,topTechs,most_used

    else:
        return empty_graphs
    
# @app.callback(
#     Output('cb-month','options',allow_duplicate=True),
#     Output('cb-month','value'),
#     Output('cb-date','options'),
#     Input('cb-year','value')
# )
# def filterMonth(year):
#     if year:
#         print(year,flush=True)
#         options = [{'label': month, 'value': month_int} for month, month_int in cube[cube["published_year"].isin(year)][["published_month", "published_month_int"]].drop_duplicates().sort_values(by='published_month_int').values] 
#         return options,[],[]
#     else:
#         return [],[],[]

# @app.callback(
#     Output('cb-date','options',allow_duplicate=True),
#     Output('cb-date','value',),
#     Input('cb-month','value')
# )
# def filterDate(month):
#     if month:
#         options = cube[cube["published_month_int"].isin(month)]["published_date"].unique()
#         return [{'label': option, 'value': option} for option in sorted(options)],[]
#     else:
#         return [],[]
    
# @app.callback(
#     Output('cb-department','options',allow_duplicate=True),
#     Output('cb-department','value'),
#     Output('cb-city','options',allow_duplicate=True),
#     Input('cb-region','value')
# )
# def filterDepartment(region):
#     if region:
#         options = cube[cube["region"].isin(region)]["department"].unique()
#         return [{'label': option, 'value': option} for option in sorted(options)],[],[]
#     else:
#         return [],[],[]

# @app.callback(
#     Output('cb-city','options',allow_duplicate=True),
#     Output('cb-city','value'),
#     Input('cb-department','value')
# )
# def filterCity(department):
#     if department:
#         options = cube[cube["department"].isin(department)]["city"].unique()
#         return [{'label': option, 'value': option} for option in sorted(options)],[]
#     else:
#         return [],[]
    
@app.callback(
    Output('line-word', 'figure',allow_duplicate=True),
    Input('line-word', 'clickData')
)
def drillCalendar(clickData):
    global level
    global prevMonth
    global prevYear
    global cube

    if clickData:
        x_value = clickData['points'][0]['x']
        if level < 3:
            level+=1
            if level==2:
                prevYear = x_value
                fig = generateUsedWordEvolution(cube,level,prevYear,None)
            if level==3:
                prevMonth = x_value
                fig = generateUsedWordEvolution(cube,level,prevYear,prevMonth)
            else:
                fig = generateUsedWordEvolution(cube,level,prevYear,prevMonth) 
        return fig
    else:
        fig = generateUsedWordEvolution(cube,1,None,None) 
        return fig

@app.callback(
    Output('wc', 'figure',allow_duplicate=True),
    Input('cb-top-n-wc', 'value')
)
def topNWC(topN):
    global cube
    if topN:
        print(cube,flush=True)
        return generateWorldCloud(cube,topN)

@app.callback(
    Output('bar-top-n-tech', 'figure',allow_duplicate=True),
    Input('cb-top-n-tech', 'value')
)
def topNTech(topN):
    global cube
    if topN:
        print(topN,flush=True)
        return generateBarTechnologies(cube,topN)
    
# @app.callback(
#     Output('line-word', 'figure',allow_duplicate=True),
#     Output('btn-roll-up', 'style'),
#     Input('btn-roll-up', 'n_clicks')
# )
# def rollUpCalendar(n_clicks):
#     global level
#     global prevYear
#     global prevMonth
#     global cube 

#     if n_clicks:
#         if level > 1:
#             level-=1
#             if level==2:
#                 fig = generateUsedWordEvolution(cube,level,None,None)
#             if level==3:
#                 fig = generateUsedWordEvolution(cube,level,prevYear,None)
#             else:   
#                 style = {"display":"none"}
#                 fig = generateUsedWordEvolution(cube,level,None,None) 

#             return style,fig