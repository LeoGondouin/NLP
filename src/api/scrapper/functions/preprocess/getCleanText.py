import re

def getCleanText(text):
    infos = [item.replace("\n"," ").strip() for item in text]
    infos = [re.sub(r'\s+', ' ',item) for item in infos]
    infos = " ".join([item for item in infos if item != ''])
    return infos