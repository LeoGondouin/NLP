from fastapi import FastAPI,Request,HTTPException
from functions.fillDW import fillDW
from functions.getCube import getCube
from typing import List,Dict,Any

app = FastAPI()


@app.post("/insert/offers")
async def insertJobOffers(request: Request, data: dict):
    fillDW(data["corpus"])

@app.get("/get/offers")
async def getJobOffers(criterias: str):
    print(criterias)
    cube = getCube(criterias)
    return cube