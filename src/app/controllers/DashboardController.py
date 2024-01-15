from dash import Input, Output, State
from dash import dcc
from dash import html
from server import app
from views.dashboard.descriptive_statistics import statistics
import requests 
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
from .functions.generateDashboard import generateDashboard
from .functions.getFilterQuery import getFilterQuery

cube = None

@app.callback(
    Output('screen-menu','children',allow_duplicate = True),
    Input('menu-dashboard','n_clicks')
)
def displayGeneralStatistics(n_clicks):
    if n_clicks is not None:
        response = requests.get("http://db_api:5002/get/offers?criterias=")
        if response.status_code == 200:
            global cube
            cube = pd.DataFrame.from_records(json.loads(response.json()))
            
            graphs = generateDashboard(cube,'region')

            filters = html.Div(
                 children = [
                        dcc.Dropdown(id="cb-website",options=[{'label': website.capitalize(), 'value': website} for website in cube["website"].unique()],multi=True),
                        dcc.Dropdown(id="cb-contract-type",options=[{'label': contract_type, 'value': contract_type} for contract_type in cube["contract_type"].unique()],multi=True),
                        dcc.Dropdown(id="cb-company",options=[{'label': company, 'value': company} for company in cube["company"].unique()],multi=True),
                        html.Div(
                            id="div-calendar-hierarchy",
                            children=[
                                dcc.Dropdown(id="cb-year",options=[{'label': year, 'value': year} for year in sorted(cube["published_year"].unique())],multi=True),
                                dcc.Dropdown(id="cb-month",multi=True),
                                dcc.Dropdown(id="cb-date",multi=True),
                            ]
                        ),
                        html.Div(
                            id="div-location",
                            children=[
                                dcc.Dropdown(id="cb-region",options=[{'label': region, 'value': region} for region in sorted(cube["region"].unique())],multi=True),
                                dcc.Dropdown(id="cb-department",multi=True),
                                dcc.Dropdown(id="cb-city",multi=True),
                            ]
                        ),
                        html.Button(id='btn-filter',children='Filter',style={"margin-right":"10px"}),
                        html.Button(id='btn-clear',children='Clear filters')
                 ]
            )
                

            descriptives_stats = [
                    filters,
                    html.Div(id="div-kpi",children=graphs["kpis"]),
                    html.Div(children=[
                                html.Div([
                                    dcc.Graph(
                                        id="pie-contract-type",
                                        figure=graphs["pie-contract-type"]
                                    ),
                                    dcc.Graph(
                                        id="bar-website",
                                        figure=graphs["bar-website"]
                                    )
                                ]),
                                html.Div([
                                    dcc.Graph(
                                        id="bar-top-5-companies",
                                        figure=graphs["bar-top-5-companies"],
                                    ), 
                                    html.Div([   
                                        dcc.Dropdown(id='cb-map-hierarchy',options=[
                                                                        {'label':'Region','value':'region'},
                                                                        {'label':'Department','value':'department'},
                                                                        {'label':'City','value':'city'}
                                                                    ],
                                                    value="region"
                                                    ),
                                        dcc.Graph(
                                            id="map-offers",
                                            figure=graphs["map-offers"]
                                        ) 
                                    ]) 
                                ],style={'width':'100%'})  
                        ]
                    ,style={"display":"flex"})
            ]
        return [statistics]+descriptives_stats
    


@app.callback(
    Output('cb-month','options',allow_duplicate=True),
    Output('cb-month','value',allow_duplicate=True),
    Output('cb-date','options',allow_duplicate=True),
    Input('cb-year','value')
)
def filterMonth(year):
    if year:
        options = [{'label': month, 'value': month_int} for month, month_int in cube[cube["published_year"].isin(year)][["published_month", "published_month_int"]].drop_duplicates().sort_values(by='published_month_int').values] 
        return options,[],[]
    else:
        return [],[],[]

@app.callback(
    Output('cb-date','options',allow_duplicate=True),
    Output('cb-date','value',allow_duplicate=True),
    Input('cb-month','value')
)
def filterDate(month):
    if month:
        options = cube[cube["published_month_int"].isin(month)]["published_date"].unique()
        return [{'label': option, 'value': option} for option in sorted(options)],[]
    else:
        return [],[]
    
@app.callback(
    Output('cb-department','options',allow_duplicate=True),
    Output('cb-department','value',allow_duplicate=True),
    Output('cb-city','options',allow_duplicate=True),
    Input('cb-region','value')
)
def filterDepartment(region):
    if region:
        options = cube[cube["region"].isin(region)]["department"].unique()
        return [{'label': option, 'value': option} for option in sorted(options)],[],[]
    else:
        return [],[],[]

@app.callback(
    Output('cb-city','options',allow_duplicate=True),
    Output('cb-city','value',allow_duplicate=True),
    Input('cb-department','value')
)
def filterCity(department):
    if department:
        options = cube[cube["department"].isin(department)]["city"].unique()
        return [{'label': option, 'value': option} for option in sorted(options)],[]
    else:
        return [],[]
    
@app.callback(
    Output('div-kpi','children',allow_duplicate=True),
    Output('bar-website','figure',allow_duplicate=True),
    Output('pie-contract-type','figure',allow_duplicate=True),
    Output('bar-top-5-companies','figure',allow_duplicate=True),
    Output('map-offers','figure',allow_duplicate=True),   
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
   
    State('cb-map-hierarchy','value')
)
def filter(n_clicks,websites,contract_types,companies,years,months,date,region,department,city,hierarchy):
    if n_clicks is not None:
        url = "http://db_api:5002/get/offers?criterias="

        fullUrl = getFilterQuery(url,websites,contract_types,companies,years,months,date,region,department,city)

        response = requests.get(fullUrl)

        fig = px.scatter_geo(
            
            )
        fig.update_layout(
            title='Aucune donnée disponible',
            coloraxis_colorbar=dict(title='Nombre d\'offres'),
            geo=dict(
                lonaxis_range=[-5.142, 9.662],
                lataxis_range=[41.303, 51.124],
                showland=True,
                landcolor='forestgreen',  
                showcountries=True,
                countrycolor='White'
            )
        )

 
        empty_graphs = html.Span(),px.bar(
                title='No data available',
                labels={'x': 'Website', 'y': 'Count'}
            ),px.pie(
                title='No data available',
                labels={'x': 'Contract Type', 'y': 'Count'}
            ),px.bar(
                title='No data available',
                labels={'y': 'Companies', 'x': 'Count'},
                orientation="h"
            ),fig
        
        if response.status_code == 200:
            cube = pd.DataFrame.from_records(json.loads(response.json()))
            if cube.shape[0]>0:
                graphs = generateDashboard(cube,hierarchy)
                return graphs["kpis"],graphs["bar-website"],graphs["pie-contract-type"],graphs["bar-top-5-companies"],graphs["map-offers"]
            else:
                return empty_graphs
            
    if cube.shape[0]>0:
        graphs = generateDashboard(cube,hierarchy)
        return graphs["kpis"],graphs["bar-website"],graphs["pie-contract-type"],graphs["bar-top-5-companies"],graphs["map-offers"]

    else:
        return empty_graphs
    
@app.callback(
    Output('div-kpi','children',allow_duplicate=True),
    Output('bar-website','figure',allow_duplicate=True),
    Output('pie-contract-type','figure',allow_duplicate=True),
    Output('bar-top-5-companies','figure',allow_duplicate=True),
    Output('map-offers','figure',allow_duplicate=True),
    Output('cb-website','value',allow_duplicate=True),
    Output('cb-contract-type','value',allow_duplicate=True),
    Output('cb-company','value',allow_duplicate=True),
    Output('cb-year','value',allow_duplicate=True),
    Output('cb-month','value',allow_duplicate=True),
    Output('cb-date','value',allow_duplicate=True),
    Output('cb-region','value',allow_duplicate=True),
    Output('cb-department','value',allow_duplicate=True),
    Output('cb-city','value',allow_duplicate=True), 
    Output('cb-month','options',allow_duplicate=True),
    Output('cb-date','options',allow_duplicate=True),
    Output('cb-department','options',allow_duplicate=True),
    Output('cb-city','options',allow_duplicate=True), 
    Input('btn-clear','n_clicks'),
    State('cb-map-hierarchy','value')
)
def clearFilters(n_clicks,hierarchy):
    if n_clicks:
        graphs = generateDashboard(cube,hierarchy)
        return graphs["kpis"],graphs["bar-website"],graphs["pie-contract-type"],graphs["bar-top-5-companies"],graphs["map-offers"],[],[],[],[],[],[],[],[],[],[],[],[],[]

    
@app.callback( 
    Output('map-offers','figure',allow_duplicate=True),
    Output('div-kpi','children',allow_duplicate=True),
    Input('cb-map-hierarchy','value'),
    State('cb-website','value'),
    State('cb-contract-type','value'),
    State('cb-company','value'),
    State('cb-year','value'),
    State('cb-month','value'),
    State('cb-date','value'),
    State('cb-region','value'),
    State('cb-department','value'),
    State('cb-city','value'),
)   
def mapDrillDownOrRollUp(hierarchy,websites,contract_types,companies,years,month,date,region,department,city):
    if hierarchy:
        url = "http://db_api:5002/get/offers?criterias="

        fullUrl = getFilterQuery(url,websites,contract_types,companies,years,month,date,region,department,city)

        response = requests.get(fullUrl)

        if response.status_code == 200:
            cube = pd.DataFrame.from_records(json.loads(response.json()))
            if cube.shape[0]>0:
                graphs = generateDashboard(cube,hierarchy)
                return graphs["map-offers"],graphs["kpis"]
            else:
                return px.bar(
                    title='No data available',
                    labels={'y': 'Company', 'x': 'Counts'},
                    orientation="h"
                )
    if cube.shape[0]>0:
        graphs = generateDashboard(cube,hierarchy)
        return graphs["map-offers"],graphs["kpis"]
    else:
        return px.bar(
                    title='No data available',
                    labels={'y': 'Company', 'x': 'Counts'},
                    orientation="h"
                )
    

    #     PreventUpdate
    
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
#         style={"display":"none"}
#         if level==3:
#             level=2
#             fig = generateUsedWordEvolution(cube,level,prevYear,None)
#             style={"display":"block"}
#         elif level==2:
#             level=1
#             fig = generateUsedWordEvolution(cube,level,None,None)
#         else:
#             fig = generateUsedWordEvolution(cube,level,None,None)
            
#         print(level,flush=True)
#         return fig,style
#     else:
#         return None,{"display":"none"}