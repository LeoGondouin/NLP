import plotly.express as px

def generateDashboard(cube):
    website_prop = cube['website'].value_counts()
    contract_type_prop = cube['contract_type'].value_counts()
    company_prop = cube['company'].value_counts()
    # Check if there's data to display
    return px.bar(
        x=website_prop.index,
        y=website_prop.values,
        title='Distribution of offers by websites',
        labels={'x': 'Websites', 'y': 'Count'}
    ),px.pie(
        names=contract_type_prop.index,
        values=contract_type_prop.values,
        title='Distribution of Contract Types',
        labels={'x': 'Websites', 'y': 'Count'}
    ),px.bar(
        x=company_prop.index[:5],
        y=company_prop.values[:5],
        title='Top 5 companies with most offers',
        labels={'x': 'Companies', 'y': 'Count'}
    )