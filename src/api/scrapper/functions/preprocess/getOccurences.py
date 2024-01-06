import json
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
from nltk.corpus import stopwords

def getOccurences(input_text):
    nlp = spacy.load("fr_core_news_sm")
    stop_words = stopwords.words('french') + stopwords.words('english')
    stop_words.extend(["être", "avoir", "faire", "aller", "pouvoir", "savoir", "devoir", "venir"])
    # french_stop_words.extend(["être", "avoir", "faire", "aller", "pouvoir", "savoir", "devoir", "venir","ête"])
    # Create TfidfVectorizer instance
    vectorizer = TfidfVectorizer(
        token_pattern=r'\b[^\d\W]+\b'
    )

    # Tokenize and transform the input text
    X = vectorizer.fit_transform([input_text])

    # Get feature names (lemmatized tokens)
    feature_names = vectorizer.get_feature_names_out()

    # Calculate TF-IDF for each term
    tfidf_values = X.sum(axis=0).A.flatten()

    lemmatized = [token.lemma_ for token in nlp(' '.join(feature_names)) if len(token.lemma_) > 1]
    stopwords_free = [word for word in lemmatized if word not in stop_words]
    # Convert token occurrences to a dictionary
    result_dict = {token: tfidf for token, tfidf in zip(stopwords_free, tfidf_values)}

    # Convert the dictionary to a stringified JSON
    json_string = json.dumps(result_dict, separators=(',', ':'), ensure_ascii=False)

    return json_string
