from fastapi import FastAPI,Request,HTTPException
from functions.scrapCorpus import scrapCorpus
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.post("/scrap/offers")
async def scrap_offers(request: Request, data: dict):  # Receive data as a dictionary
    try:
        # Access specific items within the dictionary
        keywords = data.get("keywords")
        websites = data.get("websites")
        nb_docs = data.get("nb_docs")

        # Replace this with your actual scraping logic
        scraped_corpus = scrapCorpus(websites, keywords, nb_docs)

        return JSONResponse(content=json.dumps({"status": "done", "corpus": scraped_corpus}), status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing request: {str(e)}")

