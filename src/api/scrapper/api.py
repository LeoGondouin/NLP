from fastapi import FastAPI
from typing import List
from functions import scrapCorpus
app = FastAPI()

@app.post("/scrap/offers")
async def scrapCorpus(website: List(str)):
    corpus = scrapCorpus(website)
    return corpus
