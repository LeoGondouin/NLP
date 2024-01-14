import json
from wordcloud import WordCloud
from collections import defaultdict
import plotly.express as px
from io import BytesIO
import pandas as pd

def getTotalFrequencies(line_frequencies):

    total_frequencies = defaultdict(int)
    for line_dict in line_frequencies:
        for word, frequency in line_dict.items():
            total_frequencies[word] += frequency
    total_frequencies = dict(total_frequencies)

    return total_frequencies

def generateWorldCloud(cube,topN):
    line_frequencies = [json.loads(item) for item in cube["nb_occurences"]]
    total_frequencies = getTotalFrequencies(line_frequencies)
    
    top_N_freq = {key: total_frequencies[key] for key in sorted(total_frequencies, reverse=True)[:topN]}

    wordcloud = WordCloud(width=800, height=600, background_color='white',contour_width=2).generate_from_frequencies(top_N_freq)
    fig = px.imshow(wordcloud.to_array(), binary_string=True)
    fig.update_layout(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  margin=dict(l=0, r=0, b=0, t=0))

    # Convert the Plotly Express figure to a bytes-like object
    image_bytes = BytesIO()
    fig.write_image(image_bytes, format="png",scale=5,width=800, height=600)

    return fig

def getMostUsedWord(cube):
    line_frequencies = [json.loads(item) for item in cube["nb_occurences"]]
    total_frequencies = getTotalFrequencies(line_frequencies)
    mostUsedWord = max(total_frequencies, key=total_frequencies.get)
    mostUsedWord = {mostUsedWord: total_frequencies[mostUsedWord]}
    return mostUsedWord

def generateUsedWordEvolution(cube, level, valueYear, valueMonth):
    mostUsed = dict()

    str_level = "published_year" if level == 1 else "published_month" if level == 2 else "published_day"

    ant_level = "published_year" if level == 2 else "published_month" if level == 3 else None


    if ant_level:
        if level == 2:
            sub_cube = cube[cube[ant_level] == int(valueYear)]
        elif level == 3:
            sub_cube = cube[(cube["published_year"] == int(valueYear)) & (cube[ant_level] == valueMonth)]
    else:
        sub_cube = cube

    for item in sub_cube[str_level].unique():
        mostUsed[str(item)] = getMostUsedWord(sub_cube[(sub_cube[str_level] == item)])

    sorted_mostUsed = dict(sorted(mostUsed.items()))

    # Extract keys and values for plotting
    x_year = sorted(sorted_mostUsed.keys(), key=lambda x: x)
    values = {key: value for month_dict in sorted_mostUsed.values() for key, value in month_dict.items()}
    labels = list(values.keys())
    y_count = list(values.values())

    # Create line plot with markers
    line_fig = px.line(x=x_year, y=y_count, labels={'x': str_level.capitalize(), 'y': 'Normalized TF'}, title=f'Normalized TF by {str_level.capitalize()}')

    # Add scatter points for annotations
    scatter_fig = px.scatter(x=x_year, y=y_count, text=labels)
    scatter_fig.update_traces(marker=dict(size=30))
    # Combine the two figures
    combined_fig = line_fig.update_traces(line=dict(dash='solid'))  # Set line to solid
    combined_fig.add_traces(scatter_fig.data)

    return combined_fig

def getTopTechnologies(cube,topN):
    list_techs=["C", "Cpp", "C++", "C#", "java", "javascript", "Python", "php", "SQL", "R", "Talend",
                    "SSIS", "SSAS", "Docker", "SSRS", "PowerBI", "BI" ,"Tableau" , "qlik", "excel", "ETL"]

    sub_corpus = dict()

    for i in cube.itertuples():
        corpus = eval(i.nb_occurences)
        for language in list_techs:
            if language.lower() in corpus:
                valeur = corpus[language.lower()]  # Use the language as the key
                sub_corpus[language.capitalize()] = sub_corpus.get(language, 0) + valeur

    sub_corpus = dict(sorted(sub_corpus.items(), key=lambda x: x[1], reverse=True))
    topN_techs = dict(list(sub_corpus.items())[:topN])

    return topN_techs

def generateBarTechnologies(cube,topN):
    topN_techs = getTopTechnologies(cube,topN)

    df_topN = pd.DataFrame(list(topN_techs.items()), columns=['Technology', 'Frequency'])

    fig = px.bar(df_topN, y='Technology', x='Frequency', title=f'Top {topN} Technologies')

    return fig