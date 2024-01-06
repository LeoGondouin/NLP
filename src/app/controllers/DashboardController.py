from dash import Input, Output, State
from dash import dcc
from dash import html
from server import app
from views.dashboard.descriptive_statistics import statistics
from views.dashboard.corpus_analysis import corpus_analysis

@app.callback(
    Output('screen-menu','children',allow_duplicate = True),
    Input('menu-dashboard','n_clicks'),
)
def display(n_clicks):
    if n_clicks is not None:
        return statistics
    
@app.callback(
    Output('screen-menu', 'children'),
    [Input('dashboard-tabs', 'value')]
)
def displayTab(value):
    if value=="statistics":
        return statistics
    elif value=="corpus-analysis":
        return corpus_analysis