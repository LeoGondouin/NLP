import dash_html_components as html

sidebar = html.Div(
            [
                html.Div(
                [
                    html.H1("Menu",style={"text-decoration":"underline"}),
                    html.H2(id="menu-scrapper",children = ["Scrap job offers"],className="menu-opt"),
                    html.H2(id="menu-dashboard",children = ["Descriptive statistics"],className="menu-opt"),
                    html.H2(id="menu-text-analysis",children = ["Text analysis"],className="menu-opt"),
                    html.H2(id="menu-topic-analysis",children = ["Topic analysis"],className="menu-opt")
                ],style={"margin-top": "50%"}
                )
            ]
          ,id="sidebar")