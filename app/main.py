from functools import lru_cache
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from aws.bedrock.bedrock import create_ai_summary
from aws.dynamo_db.dynamo_db import save_article
from models.schemas import ScrapeRequest, ScrapeAllRequest, DeleteDateRequest
from settings import Settings
from scraper.scraper import scrape_all_articles


app = FastAPI()

@lru_cache
def get_settings():
    return Settings()

@app.get("/")
def read_root():
    """
    Example API
    """
    return {"alive"}

@app.post("/v1/scrapeall/")
async def trigger_scrape_all(request: ScrapeAllRequest,settings: Annotated[Settings, Depends(get_settings)]):  #settings: Annotated[Settings, Depends(get_settings)]
    """
    Scrape all the articles from the list
    AI model adds the ai_summary
    Write the articles to DB
    """
    articles = await scrape_all_articles(request.urls)

    for article in articles:
        summary = create_ai_summary(article['page'],settings)
        article['ai_summary'] = summary
        save_article(article,settings)

    return JSONResponse(content=articles)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)