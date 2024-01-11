import math
from functions.preprocess.getCleanText import getCleanText
from functions.preprocess.getOccurences import getOccurences
import requests 
from bs4 import BeautifulSoup

def scrapET(keywords,nb_docs):
    source = ""
    position = ""
    company = ""
    workplace = ""
    published_date = ""
    contract_type = ""
    long_infos = ""

    corpus = list()

    pages = math.ceil(nb_docs/20)
    source = "emploi-territorial"
    rootLink = "https://www.emploi-territorial.fr"

    # 20 offres par pages
    url = f"{rootLink}/emploi-mobilite/?adv-search={keywords}&page={pages}"
    response = requests.get(url) 
    
    soup = BeautifulSoup(response.content, 'html.parser')
    root = soup.find("body")
    offresLinkElems = root.select("div[class*='bloc-lien-offre'] > a[class*='lien-details-offre']")[:nb_docs]    
    links = [rootLink+offresLinkElem.get("href") for offresLinkElem in offresLinkElems]

    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        root = soup.find("body")

        position = root.select("h2[class*='set-line-emploi']")[0].text.strip()
        company = root.select("div[class*='offre-item-value'] > strong > a")[0].text.strip() if root.select("div[class*='offre-item-value'] > strong > a") else "NULL"
        workplace = root.select_one("div[class*='offre-item-label']:contains('Lieu de travail') + .offre-item-value").text.strip() if root.select_one("div[class*='offre-item-label']:contains('Lieu de travail') + .offre-item-value") else "NULL"
        published_date = root.select_one("div[class*='px-3']:contains('Publiée le') > .set-color-green").text.strip() if root.select_one("div[class*='px-3']:contains('Publiée le') > .set-color-green") else "NULL"
        contract_type = root.select_one('div[class*="offre-item-label"]:contains("Type d\'emploi") + .offre-item-value').text.strip() if root.select_one('div[class*="offre-item-label"]:contains("Type d\'emploi") + .offre-item-value') else "NULL"
        position_type = root.select_one('div[class*="offre-item-label"]:contains("Famille de métiers") + .offre-item-value').text.split(">")[0].strip()
        
        long_infos = root.select('div[class*="offre-item-text"]')

        long_infos = getCleanText([item.text for item in long_infos])
        long_infos = getOccurences(long_infos)
        current_offer = {"source": source, "link": rootLink, "position": position, "position_type": position_type,
            "company": company, "workplace": workplace, "published_date": published_date,
            "contract_type": contract_type, "description": long_infos}
        
        corpus.append(current_offer)
    return corpus
