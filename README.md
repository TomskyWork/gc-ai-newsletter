# AI newsletter

## Packages

[Crawl4AI](https://docs.crawl4ai.com/) - LLM friendly scraper, crawler

[FastAPI](https://fastapi.tiangolo.com/) - API framework

[Uvicorn](https://www.uvicorn.org/) - Async server

python-dotenv?


## Run the project

 inside the app folder run the command to start the live server
 ```bash
 uvicorn main:app --reload
 ```

## Browser
[http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/) - shows the API endpoints 

### Test substack scraping

go to the above 'docs' url and use the POST request with the body

```json
"url" : "https://newsletter.pragmaticengineer.com/"
```

## AWS Bedrock & Langchain
https://python.langchain.com/docs/integrations/llms/bedrock/