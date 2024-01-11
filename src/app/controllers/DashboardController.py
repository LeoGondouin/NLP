from dash import Input, Output, State
from dash import dcc
from dash import html
from server import app
from views.dashboard.descriptive_statistics import statistics
from views.dashboard.corpus_analysis import corpus_analysis
import requests 
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
from .functions.generateDashboard import generateDashboard

cube = None

@app.callback(
    Output('screen-menu','children',allow_duplicate = True),
    Input('menu-dashboard','n_clicks')
)
def display(n_clicks):
    if n_clicks is not None:
        response = requests.get("http://db_api:5002/get/offers?criterias=")
        if response.status_code == 200:
            global cube
            cube = pd.DataFrame.from_records(json.loads(response.json()))

            graphs = generateDashboard(cube)

            filters = html.Div(
                 children = [
                        dcc.Dropdown(id="cb-website",options=[{'label': website.capitalize(), 'value': website} for website in cube["website"].unique()],multi=True),
                        dcc.Dropdown(id="cb-contract-type",options=[{'label': contract_type, 'value': contract_type} for contract_type in cube["contract_type"].unique()],multi=True),
                        dcc.Dropdown(id="cb-company",options=[{'label': company, 'value': company} for company in cube["company"].unique()],multi=True),
                        html.Div(
                            id="div-calendar-hierarchy",
                            children=[
                                dcc.Dropdown(id="cb-year",options=[{'label': year, 'value': year} for year in sorted(cube["published_year"].unique())],multi=True),
                                dcc.Dropdown(id="cb-month",options=[{'label': month, 'value': month} for month in cube.sort_values(['published_month_int'])["published_month"].unique()],multi=True),
                                dcc.Dropdown(id="cb-date",options=[{'label': date, 'value': date} for date in sorted(cube["published_date"].unique(), key=lambda x: datetime.strptime(x,"%Y-%m-%d"))],multi=True),
                            ]
                        ),
                        html.Div(
                            id="div-location",
                            children=[
                                dcc.Dropdown(id="cb-region",multi=True),
                                dcc.Dropdown(id="cb-departement",multi=True),
                                dcc.Dropdown(id="cb-city",options=[{'label': date, 'value': date} for date in sorted(cube["city"].unique())],multi=True),
                            ]
                        ),
                        html.Button(id='btn-filter',children='Filter')
                 ]
            )
                

            descriptives_stats = [
                    filters,
                    # html.Span(children=[
                    #                 html.Label(
                    #                     children=str(len(company_prop.index)),
                    #                     style={"font-weight":"bold"}
                    #                 ),
                    #                 " distinct count of companies"
                    #             ]
                    #         ,style={"font-size":"22px"}
                    #         ),
                    # html.Span(children=[
                    #                 html.Label(
                    #                     children=str(nb_offers),
                    #                     style={"font-weight":"bold"}
                    #                 ),
                    #                 " number of scrapped offers"
                    #             ]
                    #         ,style={"font-size":"22px","padding-left":"5px"}
                    #         ),
                    # html.Span(children=[
                    #                 html.Label(
                    #                     children=str(len(website_prop.index)),
                    #                     style={"font-weight":"bold"}
                    #                 ),
                    #                 " distinct websites count"
                    #             ]
                    #         ,style={"font-size":"22px","padding-left":"5px"}
                    #         ),
                    # html.Span(children=[
                    #                 html.Label(
                    #                     children=str(len(cube["city"].unique())),
                    #                     style={"font-weight":"bold"}
                    #                 ),
                    #                 " distinct cities count"
                    #             ]
                    #         ,style={"font-size":"22px","padding-left":"5px"}
                    #         ),
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
                                        figure=graphs["bar-top-5-companies"]
                                    )    
                                ]),
                                html.Div([
                                    dcc.Graph(
                                        id="map-offers",
                                        # figure=graphs["map-offers"]
                                    )  
                                ])  
                        ]
                    ,style={"display":"flex"})
            ]
        return [statistics]+descriptives_stats
    
def getFilterQuery(url,websites,contract_types,companies,years):
    if websites:
        if len(websites)==1:
            url += f"(website='{websites[0]}')"
        else:
            url += '('
            url += ' or '.join([f"website='{website}'" for website in websites])
            url += ')'
        url += ' and '

    if contract_types:
        if len(contract_types)==1:
            url += f"(contract_type='{contract_types[0]}')"
        else:
            url += '('
            url += ' or '.join([f"contract_type='{contract_type}'" for contract_type in contract_types])
            url += ')'
        url += ' and '

    if companies:
        if len(companies)==1:
            url += f"(company='{companies[0]}')"
        else:
            url += '('
            url += ' or '.join([f"company='{company}'" for company in companies])
            url += ')'
        url += ' and '

    if years:
        if len(years)==1:
            url += f"(year='{years[0]}')"
        else:
            url += '('
            url += ' or '.join([f"year='{year}'" for year in years])
            url += ')'
        url += ' and '

    if "and" in url.strip()[-3:]:
        url = url.strip()[:-4]

    return url

@app.callback(
    Output('bar-website','figure'),
    Output('pie-contract-type','figure'),
    Output('bar-top-5-companies','figure'),
    # Output('map-offers','figure'),   
    Input('btn-filter','n_clicks'),
    State('cb-website','value'),
    State('cb-contract-type','value'),
    State('cb-company','value'),
    State('cb-year','value')
)
def filter(n_clicks,websites,contract_types,companies,years):
    if n_clicks is not None:
        url = "http://db_api:5002/get/offers?criterias="

        fullUrl = getFilterQuery(url,websites,contract_types,companies,years)

        response = requests.get(fullUrl)

        if response.status_code == 200:
            cube = pd.DataFrame.from_records(json.loads(response.json()))
            if cube.shape[0]>0:
                graphs = generateDashboard(cube)
                return graphs["bar-website"],graphs["pie-contract-type"],graphs["bar-top-5-companies"]
            # ,graphs["map-offers"]
            else:
                return px.bar(
                    title='No data available',
                    labels={'x': 'Website', 'y': 'Count'}
                ),px.pie(
                    title='No data available',
                    labels={'x': 'Contract Type', 'y': 'Count'}
                ),px.bar(
                    title='No data available',
                    labels={'y': 'Companies', 'x': 'Count'},
                    orientation="h"
                )


    # Return an empty figure or None if conditions are not met
    if cube.shape[0]>0:
        graphs = generateDashboard(cube)
        return graphs["bar-website"],graphs["pie-contract-type"],graphs["bar-top-5-companies"]
    # ,graphs["map-offers"]
    else:
        return px.bar(
            title='No data available',
            labels={'x': 'Website', 'y': 'Counts'}
        ),px.pie(
            title='No data available',
            labels={'x': 'Contract type', 'y': 'Counts'}
        ),px.bar(
            title='No data available',
            labels={'y': 'Company', 'x': 'Counts'},
            orientation="h"
        )