from functions.sub_functions.scrapApec import scrapApec
from functions.sub_functions.scrapET import scrapET
from functions.sub_functions.scrapHW import scrapHW
from functions.sub_functions.scrapPE import scrapPE
from functions.sub_functions.scrapWTTJ import scrapWTTJ


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
    
    if 'welcometothejungle' in websites:
        corpus.extend(scrapWTTJ(keywords,nb_docs))

    print(set([item["source"] for item in corpus]))
    return corpus