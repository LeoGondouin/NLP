from fastapi import FastAPI
from functions.fillDW import fillDW
from functions.getCube import getCube
from typing import List,Dict,Any

app = FastAPI()


@app.post("/insert/offers")
async def insertJobOffers(corpus: List[Dict[str, Any]]):
    fillDW(corpus)

@app.get("/get/offers")
async def getJobOffers():
    cube = getCube()
    return cube