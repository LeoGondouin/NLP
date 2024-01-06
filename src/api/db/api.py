from fastapi import FastAPI
from src.api.models import *
from functions import fillDW,getCube
from typing import List

app = FastAPI()


@app.post("/insert/offers")
async def insertJobOffers(corpus: List(dict)):
    fillDW(corpus)

@app.get("/get/offers")
async def getJobOffers():
    cube = getCube()
    return cube