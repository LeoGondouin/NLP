import dash_html_components as html
from views.includes.sidebar import sidebar
# from views.visualization.dashboard import dashboard

# Main Layout (Two columns: Inputs / Chart)
main_layout = html.Div([
    sidebar,
    html.Div(id="screen-menu",className="screen-menu"),
], className="container")

