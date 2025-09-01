from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from aws.bedrock.bedrock import create_ai_summary
from aws.dynamo_db.dynamo_db import save_article
from models.schemas import ScrapeRequest, ScrapeAllRequest, DeleteDateRequest
from settings import Settings

from scraper.scraper import scrape_url, scrape_all_articles


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

@app.post("/v1/urlsummary/")
async def trigger_scrape(request: ScrapeRequest):
    """
    Scrape the articles API
    could come with more params later how old they should me, what topics to pick.. .etc
    """
    success = await scrape_url(request.url)

    return JSONResponse(content=success)

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


# @app.post("/v1/maintenance/")
# async def trigger_scrape_all(request: DeleteDateRequest):
#     """
#     Removes the articles from dynamo that are older than 1 month (or as needed)
#     """
#     success = await run_maintenance(request.date)
#
#     return JSONResponse(content=success)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)