import plotly.express as px
import json
import pandas as pd

def generateDashboard(cube,mapLevel):
    website_prop = cube['website'].value_counts()
    contract_type_prop = cube['contract_type'].value_counts()   
    company_prop = cube['company'].value_counts().sort_values(ascending=False).head(5)

    sub_cube = cube[~cube.isnull().any(axis=1)]
    sub_cube['latitude'] = pd.Series([item for item in sub_cube['latitude']])
    sub_cube['longitude'] = pd.Series([item for item in sub_cube['longitude']])

    mean_values = sub_cube.groupby(mapLevel)[['latitude', 'longitude']].transform('mean')
    sub_cube['latitude'] = mean_values['latitude']
    sub_cube['longitude'] = mean_values['longitude']

    sub_cube = sub_cube.groupby(['latitude','longitude',mapLevel]).size().reset_index(name='count')

    sub_cube['text'] = mapLevel.capitalize() + ' : ' + sub_cube[mapLevel] + '<br>' + 'Nb offres : ' + sub_cube['count'].astype(str)

    fig = px.scatter_geo(sub_cube,
                        lat='latitude',
                        lon='longitude',
                        color='count',
                        size='count',
                        hover_data='text',
                        hover_name=None,
                        color_continuous_scale='plasma',
                        custom_data=[mapLevel, 'count']
                    )
    fig.update_traces(textposition='top center')
    
    fig.update_layout(
        title='Nombre d\'offres en France',
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
    return {
        "bar-website":
        px.bar(
            x=website_prop.index,
            y=website_prop.values,
            title='Distribution of offers by websites',
            labels={'x': 'Websites', 'y': 'Count'}
        ),
        "pie-contract-type":
        px.pie(
            names=contract_type_prop.index,
            values=contract_type_prop.values,
            title='Distribution of Contract Types',
            labels={'x': 'Websites', 'y': 'Count'}
        ),
        "bar-top-5-companies":
        px.bar(
            y=company_prop.index,
            x=company_prop.values,
            title='Top 5 companies with most offers',
            labels={'y': 'Companies', 'x': 'Count'},
            orientation="h"
        ),
        "map-offers":fig
    }