import plotly.express as px
import json
import pandas as pd

def generateDashboard(cube):
    website_prop = cube['website'].value_counts()
    contract_type_prop = cube['contract_type'].value_counts()
    company_prop = cube['company'].value_counts().sort_values(ascending=False).head(5)

    sub_cube = cube[~cube.isnull().any(axis=1)]
    sub_cube['latitude'] = pd.Series([json.loads(item)['latitude'] for item in sub_cube['coords']])
    sub_cube['longitude'] = pd.Series([json.loads(item)['longitude'] for item in sub_cube['coords']])
    map_prop = sub_cube.groupby(['latitude','longitude']).size().reset_index(name='count')

    return {"bar-website":px.bar(
        x=website_prop.index,
        y=website_prop.values,
        title='Distribution of offers by websites',
        labels={'x': 'Websites', 'y': 'Count'}
    ),"pie-contract-type":px.pie(
        names=contract_type_prop.index,
        values=contract_type_prop.values,
        title='Distribution of Contract Types',
        labels={'x': 'Websites', 'y': 'Count'}
    ),"bar-top-5-companies":px.bar(
        y=company_prop.index,
        x=company_prop.values,
        title='Top 5 companies with most offers',
        labels={'y': 'Companies', 'x': 'Count'},
        orientation="h"
    ),"map-offers":px.scatter_geo(data_frame=map_prop, lat='latitude', lon='longitude',hover_name=None,
                color='count',  # Utilisez la valeur foncière pour la couleur des points
                color_continuous_scale='plasma'  # Palette de couleur
            )
    }