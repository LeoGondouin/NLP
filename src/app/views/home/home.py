import dash_html_components as html

home_screen = html.Div(children=[
    html.H1(children='Welcome to Job Scrapping'),

    html.P(children='Job Scrapping provides a powerful platform for scraping job offers and gaining insightful overviews through a combination of interactive dashboards, text analysis, and topic analysis. Whether you\'re a job seeker, recruiter, or data enthusiast, our app empowers you with valuable insights into the job market.'),

    html.Div(children=[
        html.H2(children='Key Features:'),
        html.Ul(children=[
            html.Li(children='🌐  Scrap Offers: Effortlessly collect job offers from various sources.'),
            html.Li(children='📊  Interactive Dashboards: Visualize and explore job market trends with dynamic and intuitive dashboards.'),
            html.Li(children='📈  Text Analysis: Uncover valuable information within job descriptions using advanced text analysis techniques.'),
            html.Li(children='🔍  Topic Analysis: Gain a deeper understanding of job market topics through insightful topic analysis.')
        ])
    ]),

    html.H2(children='How to Use:'),
    html.Ol(children=[
        html.Li(children='1.  Scrap Offers: Start by scraping job offers from your preferred websites.'),
        html.Li(children='2.  Explore Dashboards: Navigate through interactive dashboards to analyze trends and patterns.'),
        html.Li(children='3.  Text Analysis: Dive into detailed text analysis to extract meaningful insights from job descriptions.'),
        html.Li(children='4.  Topic Analysis: Explore topic analysis to identify key themes in the job market.')
    ]),

    html.P(children='Ready to embark on a data-driven journey into the job market? Let\'s get started!')
],style={"margin-left":"20%"})