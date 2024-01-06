from functions.sub_functions import scrapApec,scrapET,scrapHW,scrapPE,scrapWTTJ


def scrapCorpus(websites,keywords,nb_docs):
    
    corpus = list()

    if 'apec' in websites:
        corpus.extend(scrapApec(keywords,nb_docs))
    
    if 'emploi-territorial' in websites:
        corpus.extend(scrapET(keywords,nb_docs))
    
    if 'hellowork' in websites:
        corpus.extend(scrapHW(keywords,nb_docs))

    if 'pole-emploi' in websites:
        corpus.extend(scrapPE(keywords,nb_docs))
    
    if 'welcometothejungle':
        corpus.extend(scrapWTTJ(keywords,nb_docs))
    
    return corpus