import dash_html_components as html
import dash_core_components as dcc

corpus_analysis = html.Div(
    children=[
        html.H1('Corpus analysis'),
        dcc.Tabs(id='dashboard-tabs',value="corpus-analysis",children=[
                dcc.Tab(id="statistics",label='Descriptive statistics', value='statistics'),
                dcc.Tab(id="corpus-analysis",label='Corpus analysis', value='corpus-analysis'),
            ],style={"padding-left":"3px"})
    ],
    style={'margin-bottom': '20px'}
)
