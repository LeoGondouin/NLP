from sklearn.cluster import KMeans
import pandas as pd 
import plotly.express as px
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import json

def generateScatterClusters(cube, subject, n_clusters):
    cube['json_nbOcc'] = cube['nb_occurences'].apply(json.loads)

    corpus_liste = []

    for index, row in cube.iterrows():
        keywords = [key for key in row['json_nbOcc']]
        corpus_liste.append(keywords)

    cube['job_vector'] = corpus_liste
    # modèle Word2Vec
    model = Word2Vec(sentences=cube['job_vector'], vector_size=100, window=5, min_count=1, workers=4)

    # Fonction qui calcule le vecteur d'un document à l'aide des vecteurs des mots le constituant
    def document_vector(doc):
        word_vectors = [model.wv[word] for word in doc if word in model.wv]
        return sum(word_vectors) / len(word_vectors) if word_vectors else [0] * model.vector_size

    # Transformation des documents en vecteurs
    document_vectors = [document_vector(doc) for doc in cube['job_vector']]

    # Réduction de dimension avec PCA
    pca = PCA(n_components=2)
    F = pca.fit_transform(document_vectors)

    dfFact = pd.DataFrame(F, columns=['F1', 'F2'])

    # K-means sur les axes factoriels
    km = KMeans(n_clusters=n_clusters)
    groupes = km.fit_predict(document_vectors)

    dfFact['groupes'] = groupes

    dfFact["text"] = cube[subject]

    fig = px.scatter(
        dfFact, 
        x="F1", 
        y="F2", 
        color="groupes",
        hover_data="text",
        color_discrete_sequence=px.colors.qualitative.Set1,
        opacity=0.8
    )
    
    return fig 

