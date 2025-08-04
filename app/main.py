from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.scraper import scrape_url


class ScrapeRequest(BaseModel):
    url: str
app = FastAPI()

@app.get("/")
def read_root():
    """
    Example API
    """
    return {"Hello": "woozzaaaald"}

@app.post("/v1/scrape/")
def trigger_scrape(request: ScrapeRequest):
    success = scrape_url(request.url)

    return JSONResponse(content=success)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)