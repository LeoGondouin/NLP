from fastapi import FastAPI,Request,HTTPException
from functions import scrapCorpus

app = FastAPI()

@app.post("/scrap/offers")
async def scrapCorpus(request: Request):
    try:
        json_data = await request.json()

        # Access specific items within the JSON data
        keywords = json_data.get("keywords")
        websites = json_data.get("websites")
        nb_docs = json_data.get("param3")

        corpus = scrapCorpus(websites,keywords,nb_docs)
        return corpus

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {str(e)}")

